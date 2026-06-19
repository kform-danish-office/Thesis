#include <Arduino.h>
#include <EEPROM.h>
#include <math.h>
#include <string.h>

// ============================================================
// STM32G071 LLC / GaN primary-power controller
//
// Firmware version:
//   PWR-1.8.1 = keeps TIM1 carrier running and synchronizes only PA10 EN edges.
//   PWR-1.8.0 = carrier-synchronizes EN bursts and adds GATELEAD driver wake blanking.
//   PWR-1.7.2 = makes minimum EN burst carrier-cycle count adjustable; default 8 cycles.
//   PWR-1.7.1 = enforces nonzero EN pulses long enough for one full half-bridge carrier cycle.
//   PWR-1.7.0 = uses ADC1 DMA circular sampling only; no blocking analogRead path.
//   PWR-1.6.0 = replaces PI power control with fixed-frequency bang-bang control.
//   PWR-1.5.2 = defaults to secondary-side power feedback, PA1*PA2.
//   PWR-1.5.1 = accepts CR, LF, and CRLF UART command endings for Tera Term.
//   PWR-1.5.0 = selectable power feedback source:
//               PA0*PA2 primary V/I or PA1*PA2 secondary-voltage/current proxy.
//   PWR-1.4.0 = defers EEPROM writes while output is active to avoid UART SET freezes.
//
// Fixed carrier:
//   PA8 / PA9 = 1 MHz complementary-ish gate carrier from TIM1.
//
// Power throttle:
//   PA10 = EN burst throttle. Default EN frequency is 10 kHz.
//   Control changes PA10 high time / duty, not the 1 MHz carrier.
//
// Feedback:
//   PA0 = primary voltage divider into MCU ADC, diagnostic / optional mode
//   PA1 = isolated secondary voltage monitor, default power feedback voltage
//   PA2 = current monitor proportional to secondary output current
//
// Objective:
//   regulate selected feedback power; default is Vsec * secondary-current feedback.
//   Secondary voltage is also guarded: desired band 10..28 V, OVP 31 V.
// ============================================================

// -------------------- Pins --------------------
#define HIGH_GATE_PIN PA8
#define LOW_GATE_PIN  PA9
#define EN_PIN        PA10

#define SENSE_VPRI_PIN    PA0
#define SENSE_VOUT_PIN    PA1
#define SENSE_CURRENT_PIN PA2

#define LED_OPEN_PIN   PB13
#define LED_CLOSED_PIN PB14
#define LED_SYS_PIN    PB15

#define CMD_UART_BAUD            115200UL
#define CMD_UART_EXTERNAL_RX_PIN PC5
#define CMD_UART_EXTERNAL_TX_PIN PC4
HardwareSerial CmdSerial(CMD_UART_EXTERNAL_RX_PIN, CMD_UART_EXTERNAL_TX_PIN); // RX, TX

// -------------------- Firmware version --------------------
#define FW_VERSION_MAJOR 1
#define FW_VERSION_MINOR 8
#define FW_VERSION_PATCH 1
#define FW_VERSION_STRING "PWR-1.8.1"

// -------------------- Fixed gate settings --------------------
#define GATE_FREQ_HZ       1000000UL
#define GATE_DEADTIME_NS   40UL
#define KEEP_GATE_PWM_RUNNING 1

// -------------------- Hard limits --------------------
#define ADC_RESOLUTION_BITS 12
#define ADC_MAX_COUNTS      ((1UL << ADC_RESOLUTION_BITS) - 1UL)

#define EN_FREQ_MIN_HARD_HZ     1000UL
#define EN_FREQ_MAX_HARD_HZ    50000UL
#define EN_MIN_EDGE_HARD_US        1UL
#define EN_MAX_EDGE_HARD_US       20UL
#define EN_MIN_GATE_CYCLES_MIN     1UL
#define EN_MIN_GATE_CYCLES_MAX    40UL
#define EN_GATE_LEAD_CYCLES_MIN    0UL
#define EN_GATE_LEAD_CYCLES_MAX   40UL
#define EN_GATE_TAIL_CYCLES        1UL

#define DUTY_X10_MIN              0
#define DUTY_X10_MAX           1000

#define POWER_TARGET_MIN_W       0.5f
#define POWER_TARGET_MAX_W    2000.0f

#define SEC_V_MIN_HARD          0.0f
#define SEC_V_MAX_HARD         80.0f

#define CONTROL_PERIOD_MIN_US    50UL
#define CONTROL_PERIOD_MAX_US 20000UL

#define EEPROM_MAGIC       0x50575239UL  // "PWR9"
#define EEPROM_MAGIC_NAME  "PWR9"
#define EEPROM_SLOT_COUNT  4
#define EEPROM_BASE_ADDR   0

#define UART_INPUT_MAX_CHARS 96
#define UART_BYTES_PER_LOOP_ACTIVE 32
#define UART_BYTES_PER_LOOP_IDLE   96
#define EEPROM_DEFER_QUIET_MS 1500UL

#define LED_ACTIVE_LOW false

// -------------------- Defaults --------------------
#define DEFAULT_SYSTEM_ENABLED      0
#define DEFAULT_CONTROL_MODE        MODE_OPEN_LOOP
#define DEFAULT_POWER_FEEDBACK_MODE PFB_SECONDARY_VI

#define DEFAULT_ADC_REF_V           3.300f

// PA0 primary divider recommendation for 450 V peak:
// Rtop = 1.50 Mohm, Rbottom = 10.0 kohm. PA0 ~= Vin / 151,
// so 450 V peak reads about 2.98 V with a 3.3 V ADC reference.
// Populate Rtop as several series resistors for voltage and power sharing.
#define DEFAULT_VPRI_TOP_K        1500.0f
#define DEFAULT_VPRI_BOTTOM_K       10.0f

// PA1 isolated secondary sense, same hardware as prior firmware.
#define DEFAULT_AMC_REFIN_V          3.300f
#define DEFAULT_AMC_VCLIP_V          1.280f
#define DEFAULT_VSEC_TOP_K         390.0f
#define DEFAULT_VSEC_BOTTOM_K       10.0f

// PA2 current sense. 820 ohm is the added pull/load value on the sensor output.
// Scale CSGAIN so PA2 reports equivalent secondary output amps.
#define DEFAULT_CS_RES_OHMS        820.0f
#define DEFAULT_CS_GAIN_A_PER_A      0.000901f

#define DEFAULT_POWER_TARGET_W       50.0f
#define DEFAULT_EN_FREQ_HZ        10000UL
#define DEFAULT_EN_FREQ_MIN_HZ     5000UL
#define DEFAULT_EN_FREQ_MAX_HZ    50000UL
#define DEFAULT_EN_PREF_HZ        10000UL
#define DEFAULT_EN_FREQ_PENALTY_W    2.0f
#define DEFAULT_EN_MIN_EDGE_US        2UL
#define DEFAULT_EN_MIN_GATE_CYCLES    8UL
#define DEFAULT_EN_GATE_LEAD_CYCLES   0UL

#define DEFAULT_OPEN_DUTY_X10         0
#define DEFAULT_BIAS_DUTY_X10       120   // 12.0%
#define DEFAULT_POWERUP_DUTY_X10     80   // 8.0%
#define DEFAULT_DUTY_MIN_X10          0
#define DEFAULT_DUTY_MAX_X10        900   // 90.0%
#define DEFAULT_ALLOW_STATIC_100      0

#define DEFAULT_PRECHARGE_ENABLE      1
#define DEFAULT_PRECHARGE_DUTY_X10    1    // 0.1% average; low-duty pulse skipping preserves average energy
#define DEFAULT_PRECHARGE_BURST_MS    3UL
#define DEFAULT_PRECHARGE_SETTLE_MS  80UL
#define DEFAULT_PRECHARGE_MAX_BURSTS  4
#define DEFAULT_PRECHARGE_READY_V     4.0f
#define DEFAULT_PRECHARGE_TUNE_MAX_DUTY_X10 20 // 2.0%
#define DEFAULT_PRECHARGE_TUNE_MAX_BURSTS   20

#define DEFAULT_CONTROL_PERIOD_US   200UL // 5 kHz requested loop
#define DEFAULT_STATUS_MS          500UL
#define DEFAULT_ADC_VPRI_SAMPLES      2
#define DEFAULT_ADC_VSEC_SAMPLES      2
#define DEFAULT_ADC_I_SAMPLES         2
#define DEFAULT_ADC_DUMMY             1
#define DEFAULT_POWER_TAU_MS          2.0f
#define DEFAULT_VPRI_TAU_MS           2.0f
#define DEFAULT_CURRENT_TAU_MS        2.0f
#define DEFAULT_VSEC_TAU_MS           3.0f

#define DEFAULT_KP_X1000            250L  // 0.250 %/W
#define DEFAULT_KI_X1000           1500L  // 1.500 %/(W*s)
#define DEFAULT_DEADBAND_MW       2000L   // 2.000 W; bang-bang hysteresis fallback
#define DEFAULT_SLEW_X10_PER_SEC  3000L   // 300.0 %/s
#define DEFAULT_INT_MIN_X10       -600L
#define DEFAULT_INT_MAX_X10        600L

#define DEFAULT_SEC_MIN_V          10.0f
#define DEFAULT_SEC_MAX_V          28.0f
#define DEFAULT_SEC_OVP_V          31.0f
#define DEFAULT_SEC_OVP_ENABLE        1
#define DEFAULT_SEC_LOW_BOOST_PCT_V  12.0f
#define DEFAULT_SEC_HIGH_FOLD_PCT_V  10.0f

#define DEFAULT_CURRENT_TRIP_ENABLE   1
#define DEFAULT_CURRENT_TRIP_A        8.00f
#define DEFAULT_CURRENT_SOFT_A        6.50f
#define DEFAULT_CURRENT_FOLDBACK_EN   1
#define DEFAULT_CURRENT_FOLD_PCT_A   12.0f
#define DEFAULT_CURRENT_ABS_MODE       1

#define DEFAULT_MAX_DUTY_FAULT_EN     0
#define DEFAULT_MAX_DUTY_FAULT_MS  1200UL
#define DEFAULT_MAX_DUTY_ERR_MW    3000L

#define DEFAULT_AUTOTUNE_MAX_DUTY_X10  850
#define DEFAULT_AUTOTUNE_COARSE_X10     20   // 2.0%
#define DEFAULT_AUTOTUNE_FINE_X10        5   // 0.5%
#define DEFAULT_AUTOTUNE_SETTLE_MS     160UL
#define DEFAULT_AUTOTUNE_MEASURE_MS    100UL
#define DEFAULT_AUTOTUNE_TEST_X10       20   // 2.0%
#define DEFAULT_AUTOTUNE_FREQ_STEP_HZ 2000UL

#define DEFAULT_BANG_LOW_DUTY_X10      0   // off/idle throttle
#define DEFAULT_BANG_HIGH_DUTY_X10   120   // calibrated high throttle, default 12.0%
#define DEFAULT_BANG_HYST_MW        2000L  // +/- 2.0 W around PTARGET
#define DEFAULT_BANG_MIN_ON_MS         2UL
#define DEFAULT_BANG_MIN_OFF_MS        2UL

#define CAL_LOAD_SLOT_COUNT              3
#define DEFAULT_CAL_LOAD1_OHMS          10.0f
#define DEFAULT_CAL_LOAD2_OHMS           5.0f
#define DEFAULT_CAL_LOAD3_OHMS           2.5f

// ============================================================
// Types
// ============================================================

enum ControlMode : uint8_t {
  MODE_OPEN_LOOP = 0,
  MODE_POWER_LOOP = 1
};

enum PowerFeedbackMode : uint8_t {
  PFB_PRIMARY_VI = 0,
  PFB_SECONDARY_VI = 1
};

enum FaultCode : uint8_t {
  FAULT_NONE = 0,
  FAULT_CURRENT = 1,
  FAULT_OVP = 2,
  FAULT_SENSOR = 3,
  FAULT_MAX_DUTY = 4
};

enum StartupPhase : uint8_t {
  STARTUP_IDLE = 0,
  STARTUP_BURST = 1,
  STARTUP_SETTLE = 2
};

struct __attribute__((packed)) SettingsSlot {
  uint32_t magic;
  uint32_t sequence;

  uint8_t systemEnabled;
  uint8_t controlMode;
  uint8_t allowStatic100;
  uint8_t currentAbsMode;
  uint8_t powerFeedbackMode;
  uint8_t prechargeEnable;
  uint8_t prechargeMaxBursts;
  uint8_t prechargeTuneMaxBursts;

  uint16_t openLoopDutyX10;
  uint16_t biasDutyX10;
  uint16_t powerupDutyX10;
  uint16_t dutyMinX10;
  uint16_t dutyMaxX10;
  uint16_t prechargeDutyX10;
  uint16_t prechargeTuneMaxDutyX10;
  uint16_t bangLowDutyX10;
  uint16_t bangHighDutyX10;

  uint32_t enFreqHz;
  uint32_t enFreqMinHz;
  uint32_t enFreqMaxHz;
  uint32_t enFreqPrefHz;
  uint32_t controlPeriodUs;
  uint32_t statusMs;
  uint32_t maxDutyFaultMs;
  uint32_t prechargeBurstMs;
  uint32_t prechargeSettleMs;
  uint32_t bangMinOnMs;
  uint32_t bangMinOffMs;

  uint16_t enMinEdgeUs;
  uint16_t enMinGateCycles;
  uint16_t enGateLeadCycles;
  uint16_t adcVpriSamples;
  uint16_t adcVsecSamples;
  uint16_t adcISamples;
  uint16_t adcDummy;

  float adcRefV;
  float prechargeReadyV;
  float vpriTopK;
  float vpriBottomK;
  float vpriGain;
  float vpriOffsetV;

  float amcRefV;
  float amcVclipV;
  float vsecTopK;
  float vsecBottomK;
  float vsecGain;
  float vsecOffsetV;

  float csResOhms;
  float csGainAperA;
  float currentOffsetV;
  float currentTripA;
  float currentSoftA;
  float currentFoldPctPerA;
  uint8_t currentTripEnable;
  uint8_t currentFoldbackEnable;

  float targetPowerW;
  int32_t kp_x1000;
  int32_t ki_x1000;
  int32_t deadbandMw;
  int32_t slewX10PerSec;
  int32_t integralMinX10;
  int32_t integralMaxX10;

  float powerTauMs;
  float vpriTauMs;
  float currentTauMs;
  float vsecTauMs;

  uint8_t secOvpEnable;
  float secMinV;
  float secMaxV;
  float secOvpV;
  float secLowBoostPctPerV;
  float secHighFoldPctPerV;

  uint8_t maxDutyFaultEnable;
  int32_t maxDutyFaultErrMw;
  int32_t bangHystMw;

  uint16_t autotuneMaxDutyX10;
  uint16_t autotuneCoarseStepX10;
  uint16_t autotuneFineStepX10;
  uint16_t autotuneTestStepX10;
  uint32_t autotuneSettleMs;
  uint32_t autotuneMeasureMs;
  uint32_t autotuneFreqStepHz;
  float enFreqPenaltyW;

  uint8_t activeCalLoadSlot;
  float calLoadOhms[CAL_LOAD_SLOT_COUNT];
  uint32_t calLoadFreqHz[CAL_LOAD_SLOT_COUNT];
  uint16_t calLoadDutyX10[CAL_LOAD_SLOT_COUNT];
  int32_t calLoadKp_x1000[CAL_LOAD_SLOT_COUNT];
  int32_t calLoadKi_x1000[CAL_LOAD_SLOT_COUNT];
  float calLoadGainWPerPct[CAL_LOAD_SLOT_COUNT];
  float calLoadTauS[CAL_LOAD_SLOT_COUNT];
  float calLoadTargetW[CAL_LOAD_SLOT_COUNT];
  float calLoadMeasuredW[CAL_LOAD_SLOT_COUNT];
  float calLoadMeasuredVsec[CAL_LOAD_SLOT_COUNT];
  float calLoadMeasuredI[CAL_LOAD_SLOT_COUNT];

  float tunedPlantGainWPerPct;
  float tunedPlantTauS;
  uint16_t tunedDutyX10;
  float tunedTargetW;

  uint32_t checksum;
};

struct MeasureResult {
  float avgVpri;
  float avgVsec;
  float minVsec;
  float maxVsec;
  float avgI;
  float avgP;
  float minP;
  float maxP;
  uint32_t count;
  uint32_t avgBlockUs;
  bool valid;
  bool fault;
  bool highVStop;
};

// ============================================================
// Globals
// ============================================================

SettingsSlot cfg;
uint32_t settingsSequence = 0;
int activeSlotIndex = -1;

void saveSettings();
void saveSettingsNow();
bool requestSettingsSave(const char *reason);
bool startupPrechargeActive();
void setEnFrequencyHz(uint32_t hz);
void setEnDutyX10(uint16_t dutyX10);
void setEnDutyX10BypassLimits(uint16_t dutyX10);

HardwareTimer *EnTimer = new HardwareTimer(TIM3);

volatile uint16_t enDutyCmdX10 = DEFAULT_OPEN_DUTY_X10;
volatile uint16_t enDutyEffX10 = DEFAULT_OPEN_DUTY_X10;
volatile bool enDutyLimitBypass = false;
volatile uint32_t enFreqRuntimeHz = DEFAULT_EN_FREQ_HZ;
volatile uint32_t enPeriodUs = 100;
volatile uint32_t enHighUs = 0;
volatile uint16_t enHighGateCycles = DEFAULT_EN_MIN_GATE_CYCLES;
volatile uint16_t enPulseSkipN = 1;
volatile uint16_t enPulseSkipCountdown = 0;
volatile bool enPwmStateHigh = false;
volatile uint16_t enSyncLeadCyclesLeft = 0;
volatile uint16_t enSyncDriveCyclesLeft = 0;
volatile uint16_t enSyncTailCyclesLeft = 0;
volatile uint16_t enSyncRequestedDriveCycles = DEFAULT_EN_MIN_GATE_CYCLES;
volatile bool enSyncBurstPending = false;
volatile bool enSyncCarrierActive = false;
volatile uint32_t enSyncRiseCount = 0;
volatile uint32_t enSyncDriveStartCount = 0;
volatile uint32_t enSyncFallCount = 0;
volatile uint32_t enSyncAbortCount = 0;
uint32_t enTimerAppliedHighUs = 0;
uint16_t enTimerAppliedPulseSkipN = 1;

ControlMode controlMode = MODE_OPEN_LOOP;
bool systemEnabled = false;
bool faultLatched = false;
FaultCode faultCode = FAULT_NONE;
bool settingsDirty = false;
uint32_t settingsDirtyMs = 0;

char inputLine[UART_INPUT_MAX_CHARS + 1];
uint8_t inputLen = 0;
bool uartInputActive = false;
bool lastSerialWasCr = false;
uint32_t lastUartCharMs = 0;

uint16_t rawPa0Adc = 0;
uint16_t rawPa1Adc = 0;
uint16_t rawPa2Adc = 0;
float rawPa0Voltage = 0.0f;
float rawPa1Voltage = 0.0f;
float rawPa2Voltage = 0.0f;

float latestVpriRaw = 0.0f;
float latestVsecRaw = 0.0f;
float latestCurrentRaw = 0.0f;
float latestPowerRaw = 0.0f;
float filteredVpri = 0.0f;
float filteredVsec = 0.0f;
float filteredCurrent = 0.0f;
float filteredPower = 0.0f;
bool filtersPrimed = false;

float controlDutyPercent = 0.0f;
float powerIntegratorPct = 0.0f;
uint32_t maxDutyStartMs = 0;
bool bangBangHigh = false;
uint32_t bangBangLastSwitchMs = 0;

StartupPhase startupPhase = STARTUP_IDLE;
uint32_t startupPhaseStartMs = 0;
uint8_t startupBurstCount = 0;

uint32_t lastControlDtUs = 0;
uint32_t maxControlDtUs = 0;
uint32_t controlOverrunCount = 0;
uint32_t lastAdcBlockUs = 0;
uint32_t maxAdcBlockUs = 0;
uint32_t lastAnalogUs = 0;
bool autoTuneRunning = false;
bool lastTunePointHighVStop = false;

#define ADC_DMA_CHANNEL_COUNT 3
#define ADC_DMA_VPRI_INDEX    0
#define ADC_DMA_VSEC_INDEX    1
#define ADC_DMA_I_INDEX       2

ADC_HandleTypeDef adcDmaHandle;
DMA_HandleTypeDef adcDmaHandleDma;
volatile uint16_t adcDmaBuffer[ADC_DMA_CHANNEL_COUNT] = {0, 0, 0};
bool adcDmaRunning = false;
uint32_t adcDmaStartErrors = 0;

// ============================================================
// Utility
// ============================================================

float clampFloat(float x, float lo, float hi) {
  if (x < lo) return lo;
  if (x > hi) return hi;
  return x;
}

uint32_t clampU32(uint32_t x, uint32_t lo, uint32_t hi) {
  if (x < lo) return lo;
  if (x > hi) return hi;
  return x;
}

int32_t clampI32(int32_t x, int32_t lo, int32_t hi) {
  if (x < lo) return lo;
  if (x > hi) return hi;
  return x;
}

uint16_t clampDutyX10(int32_t d) {
  if (d < DUTY_X10_MIN) return DUTY_X10_MIN;
  if (d > DUTY_X10_MAX) return DUTY_X10_MAX;
  return (uint16_t)d;
}

uint16_t dutyPercentToX10(float p) {
  p = clampFloat(p, 0.0f, 100.0f);
  return (uint16_t)(p * 10.0f + 0.5f);
}

float dutyX10ToPercent(uint16_t d) {
  return ((float)d) * 0.1f;
}

bool validLoadSlot(uint8_t slot) {
  return slot < CAL_LOAD_SLOT_COUNT;
}

float calLoadOhms(uint8_t slot) {
  if (!validLoadSlot(slot)) return 0.0f;
  if (!isfinite(cfg.calLoadOhms[slot]) || cfg.calLoadOhms[slot] <= 0.0f) return 0.0f;
  return cfg.calLoadOhms[slot];
}

float expectedLoadPowerW(uint8_t slot) {
  float r = calLoadOhms(slot);
  if (r <= 0.0f) return 0.0f;
  return cfg.targetPowerW;
}

bool loadProfileValid(uint8_t slot) {
  if (!validLoadSlot(slot)) return false;
  return cfg.calLoadTargetW[slot] > 0.0f &&
         cfg.calLoadFreqHz[slot] >= EN_FREQ_MIN_HARD_HZ &&
         cfg.calLoadDutyX10[slot] > 0;
}

void ledWrite(uint8_t pin, bool on) {
  if (LED_ACTIVE_LOW) digitalWrite(pin, on ? LOW : HIGH);
  else digitalWrite(pin, on ? HIGH : LOW);
}

void updateModeLEDs() {
  ledWrite(LED_OPEN_PIN, systemEnabled && controlMode == MODE_OPEN_LOOP && !faultLatched);
  ledWrite(LED_CLOSED_PIN, systemEnabled && controlMode == MODE_POWER_LOOP && !faultLatched);
  ledWrite(LED_SYS_PIN, systemEnabled && !faultLatched);
}

// ============================================================
// Settings / EEPROM
// ============================================================

void setDefaults() {
  memset(&cfg, 0, sizeof(cfg));
  cfg.magic = EEPROM_MAGIC;
  cfg.sequence = 0;

  cfg.systemEnabled = DEFAULT_SYSTEM_ENABLED;
  cfg.controlMode = (uint8_t)DEFAULT_CONTROL_MODE;
  cfg.allowStatic100 = DEFAULT_ALLOW_STATIC_100;
  cfg.currentAbsMode = DEFAULT_CURRENT_ABS_MODE;
  cfg.powerFeedbackMode = (uint8_t)DEFAULT_POWER_FEEDBACK_MODE;
  cfg.prechargeEnable = DEFAULT_PRECHARGE_ENABLE;
  cfg.prechargeMaxBursts = DEFAULT_PRECHARGE_MAX_BURSTS;
  cfg.prechargeTuneMaxBursts = DEFAULT_PRECHARGE_TUNE_MAX_BURSTS;

  cfg.openLoopDutyX10 = DEFAULT_OPEN_DUTY_X10;
  cfg.biasDutyX10 = DEFAULT_BIAS_DUTY_X10;
  cfg.powerupDutyX10 = DEFAULT_POWERUP_DUTY_X10;
  cfg.dutyMinX10 = DEFAULT_DUTY_MIN_X10;
  cfg.dutyMaxX10 = DEFAULT_DUTY_MAX_X10;
  cfg.prechargeDutyX10 = DEFAULT_PRECHARGE_DUTY_X10;
  cfg.prechargeTuneMaxDutyX10 = DEFAULT_PRECHARGE_TUNE_MAX_DUTY_X10;
  cfg.bangLowDutyX10 = DEFAULT_BANG_LOW_DUTY_X10;
  cfg.bangHighDutyX10 = DEFAULT_BANG_HIGH_DUTY_X10;

  cfg.enFreqHz = DEFAULT_EN_FREQ_HZ;
  cfg.enFreqMinHz = DEFAULT_EN_FREQ_MIN_HZ;
  cfg.enFreqMaxHz = DEFAULT_EN_FREQ_MAX_HZ;
  cfg.enFreqPrefHz = DEFAULT_EN_PREF_HZ;
  cfg.controlPeriodUs = DEFAULT_CONTROL_PERIOD_US;
  cfg.statusMs = DEFAULT_STATUS_MS;
  cfg.maxDutyFaultMs = DEFAULT_MAX_DUTY_FAULT_MS;
  cfg.prechargeBurstMs = DEFAULT_PRECHARGE_BURST_MS;
  cfg.prechargeSettleMs = DEFAULT_PRECHARGE_SETTLE_MS;
  cfg.bangMinOnMs = DEFAULT_BANG_MIN_ON_MS;
  cfg.bangMinOffMs = DEFAULT_BANG_MIN_OFF_MS;
  cfg.enMinEdgeUs = DEFAULT_EN_MIN_EDGE_US;
  cfg.enMinGateCycles = DEFAULT_EN_MIN_GATE_CYCLES;
  cfg.enGateLeadCycles = DEFAULT_EN_GATE_LEAD_CYCLES;

  cfg.adcVpriSamples = DEFAULT_ADC_VPRI_SAMPLES;
  cfg.adcVsecSamples = DEFAULT_ADC_VSEC_SAMPLES;
  cfg.adcISamples = DEFAULT_ADC_I_SAMPLES;
  cfg.adcDummy = DEFAULT_ADC_DUMMY;

  cfg.adcRefV = DEFAULT_ADC_REF_V;
  cfg.prechargeReadyV = DEFAULT_PRECHARGE_READY_V;
  cfg.vpriTopK = DEFAULT_VPRI_TOP_K;
  cfg.vpriBottomK = DEFAULT_VPRI_BOTTOM_K;
  cfg.vpriGain = 1.0f;
  cfg.vpriOffsetV = 0.0f;

  cfg.amcRefV = DEFAULT_AMC_REFIN_V;
  cfg.amcVclipV = DEFAULT_AMC_VCLIP_V;
  cfg.vsecTopK = DEFAULT_VSEC_TOP_K;
  cfg.vsecBottomK = DEFAULT_VSEC_BOTTOM_K;
  cfg.vsecGain = 1.0f;
  cfg.vsecOffsetV = 0.0f;

  cfg.csResOhms = DEFAULT_CS_RES_OHMS;
  cfg.csGainAperA = DEFAULT_CS_GAIN_A_PER_A;
  cfg.currentOffsetV = 0.0f;
  cfg.currentTripA = DEFAULT_CURRENT_TRIP_A;
  cfg.currentSoftA = DEFAULT_CURRENT_SOFT_A;
  cfg.currentFoldPctPerA = DEFAULT_CURRENT_FOLD_PCT_A;
  cfg.currentTripEnable = DEFAULT_CURRENT_TRIP_ENABLE;
  cfg.currentFoldbackEnable = DEFAULT_CURRENT_FOLDBACK_EN;

  cfg.targetPowerW = DEFAULT_POWER_TARGET_W;
  cfg.kp_x1000 = DEFAULT_KP_X1000;
  cfg.ki_x1000 = DEFAULT_KI_X1000;
  cfg.deadbandMw = DEFAULT_DEADBAND_MW;
  cfg.slewX10PerSec = DEFAULT_SLEW_X10_PER_SEC;
  cfg.integralMinX10 = DEFAULT_INT_MIN_X10;
  cfg.integralMaxX10 = DEFAULT_INT_MAX_X10;

  cfg.powerTauMs = DEFAULT_POWER_TAU_MS;
  cfg.vpriTauMs = DEFAULT_VPRI_TAU_MS;
  cfg.currentTauMs = DEFAULT_CURRENT_TAU_MS;
  cfg.vsecTauMs = DEFAULT_VSEC_TAU_MS;

  cfg.secOvpEnable = DEFAULT_SEC_OVP_ENABLE;
  cfg.secMinV = DEFAULT_SEC_MIN_V;
  cfg.secMaxV = DEFAULT_SEC_MAX_V;
  cfg.secOvpV = DEFAULT_SEC_OVP_V;
  cfg.secLowBoostPctPerV = DEFAULT_SEC_LOW_BOOST_PCT_V;
  cfg.secHighFoldPctPerV = DEFAULT_SEC_HIGH_FOLD_PCT_V;

  cfg.maxDutyFaultEnable = DEFAULT_MAX_DUTY_FAULT_EN;
  cfg.maxDutyFaultErrMw = DEFAULT_MAX_DUTY_ERR_MW;
  cfg.bangHystMw = DEFAULT_BANG_HYST_MW;

  cfg.autotuneMaxDutyX10 = DEFAULT_AUTOTUNE_MAX_DUTY_X10;
  cfg.autotuneCoarseStepX10 = DEFAULT_AUTOTUNE_COARSE_X10;
  cfg.autotuneFineStepX10 = DEFAULT_AUTOTUNE_FINE_X10;
  cfg.autotuneTestStepX10 = DEFAULT_AUTOTUNE_TEST_X10;
  cfg.autotuneSettleMs = DEFAULT_AUTOTUNE_SETTLE_MS;
  cfg.autotuneMeasureMs = DEFAULT_AUTOTUNE_MEASURE_MS;
  cfg.autotuneFreqStepHz = DEFAULT_AUTOTUNE_FREQ_STEP_HZ;
  cfg.enFreqPenaltyW = DEFAULT_EN_FREQ_PENALTY_W;

  cfg.activeCalLoadSlot = 0;
  cfg.calLoadOhms[0] = DEFAULT_CAL_LOAD1_OHMS;
  cfg.calLoadOhms[1] = DEFAULT_CAL_LOAD2_OHMS;
  cfg.calLoadOhms[2] = DEFAULT_CAL_LOAD3_OHMS;
  for (uint8_t i = 0; i < CAL_LOAD_SLOT_COUNT; i++) {
    cfg.calLoadFreqHz[i] = DEFAULT_EN_FREQ_HZ;
    cfg.calLoadDutyX10[i] = DEFAULT_BIAS_DUTY_X10;
    cfg.calLoadKp_x1000[i] = DEFAULT_KP_X1000;
    cfg.calLoadKi_x1000[i] = DEFAULT_KI_X1000;
    cfg.calLoadGainWPerPct[i] = 0.0f;
    cfg.calLoadTauS[i] = 0.0f;
    cfg.calLoadTargetW[i] = 0.0f;
    cfg.calLoadMeasuredW[i] = 0.0f;
    cfg.calLoadMeasuredVsec[i] = 0.0f;
    cfg.calLoadMeasuredI[i] = 0.0f;
  }

  cfg.tunedPlantGainWPerPct = 0.0f;
  cfg.tunedPlantTauS = 0.0f;
  cfg.tunedDutyX10 = DEFAULT_BIAS_DUTY_X10;
  cfg.tunedTargetW = 0.0f;
}

void validateSettings() {
  if (cfg.magic != EEPROM_MAGIC) setDefaults();

  cfg.systemEnabled = cfg.systemEnabled ? 1 : 0;
  if (cfg.controlMode > MODE_POWER_LOOP) cfg.controlMode = MODE_OPEN_LOOP;
  cfg.allowStatic100 = cfg.allowStatic100 ? 1 : 0;
  cfg.currentAbsMode = cfg.currentAbsMode ? 1 : 0;
  if (cfg.powerFeedbackMode > PFB_SECONDARY_VI) cfg.powerFeedbackMode = (uint8_t)DEFAULT_POWER_FEEDBACK_MODE;
  cfg.prechargeEnable = cfg.prechargeEnable ? 1 : 0;
  cfg.prechargeMaxBursts = (uint8_t)clampU32(cfg.prechargeMaxBursts, 1, 20);
  cfg.prechargeTuneMaxBursts = (uint8_t)clampU32(cfg.prechargeTuneMaxBursts, 1, 50);

  cfg.openLoopDutyX10 = clampDutyX10(cfg.openLoopDutyX10);
  cfg.biasDutyX10 = clampDutyX10(cfg.biasDutyX10);
  cfg.powerupDutyX10 = clampDutyX10(cfg.powerupDutyX10);
  cfg.dutyMinX10 = clampDutyX10(cfg.dutyMinX10);
  cfg.dutyMaxX10 = clampDutyX10(cfg.dutyMaxX10);
  cfg.prechargeDutyX10 = clampDutyX10(cfg.prechargeDutyX10);
  cfg.prechargeTuneMaxDutyX10 = clampDutyX10(cfg.prechargeTuneMaxDutyX10);
  cfg.bangLowDutyX10 = clampDutyX10(cfg.bangLowDutyX10);
  cfg.bangHighDutyX10 = clampDutyX10(cfg.bangHighDutyX10);
  if (cfg.dutyMaxX10 < cfg.dutyMinX10 + 10) cfg.dutyMaxX10 = cfg.dutyMinX10 + 10;
  if (cfg.dutyMaxX10 > DUTY_X10_MAX) cfg.dutyMaxX10 = DUTY_X10_MAX;
  if (cfg.prechargeTuneMaxDutyX10 < cfg.prechargeDutyX10) cfg.prechargeTuneMaxDutyX10 = cfg.prechargeDutyX10;
  if (cfg.bangLowDutyX10 < cfg.dutyMinX10) cfg.bangLowDutyX10 = cfg.dutyMinX10;
  if (cfg.bangLowDutyX10 >= cfg.dutyMaxX10) cfg.bangLowDutyX10 = cfg.dutyMinX10;
  if (cfg.bangHighDutyX10 < cfg.bangLowDutyX10 + 1) cfg.bangHighDutyX10 = cfg.bangLowDutyX10 + 1;
  if (cfg.bangHighDutyX10 > cfg.dutyMaxX10) cfg.bangHighDutyX10 = cfg.dutyMaxX10;

  cfg.enFreqMinHz = clampU32(cfg.enFreqMinHz, EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
  cfg.enFreqMaxHz = clampU32(cfg.enFreqMaxHz, EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
  if (cfg.enFreqMaxHz < cfg.enFreqMinHz) cfg.enFreqMaxHz = cfg.enFreqMinHz;
  cfg.enFreqHz = clampU32(cfg.enFreqHz, cfg.enFreqMinHz, cfg.enFreqMaxHz);
  cfg.enFreqPrefHz = clampU32(cfg.enFreqPrefHz, EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
  cfg.enMinEdgeUs = (uint16_t)clampU32(cfg.enMinEdgeUs, EN_MIN_EDGE_HARD_US, EN_MAX_EDGE_HARD_US);
  cfg.enMinGateCycles = (uint16_t)clampU32(cfg.enMinGateCycles, EN_MIN_GATE_CYCLES_MIN, EN_MIN_GATE_CYCLES_MAX);
  cfg.enGateLeadCycles = (uint16_t)clampU32(cfg.enGateLeadCycles, EN_GATE_LEAD_CYCLES_MIN, EN_GATE_LEAD_CYCLES_MAX);

  cfg.controlPeriodUs = clampU32(cfg.controlPeriodUs, CONTROL_PERIOD_MIN_US, CONTROL_PERIOD_MAX_US);
  cfg.statusMs = clampU32(cfg.statusMs, 100UL, 5000UL);
  cfg.maxDutyFaultMs = clampU32(cfg.maxDutyFaultMs, 50UL, 10000UL);
  cfg.prechargeBurstMs = clampU32(cfg.prechargeBurstMs, 1UL, 500UL);
  cfg.prechargeSettleMs = clampU32(cfg.prechargeSettleMs, 1UL, 2000UL);
  cfg.bangMinOnMs = clampU32(cfg.bangMinOnMs, 0UL, 1000UL);
  cfg.bangMinOffMs = clampU32(cfg.bangMinOffMs, 0UL, 1000UL);

  cfg.adcVpriSamples = (uint16_t)clampU32(cfg.adcVpriSamples, 1, 64);
  cfg.adcVsecSamples = (uint16_t)clampU32(cfg.adcVsecSamples, 1, 64);
  cfg.adcISamples = (uint16_t)clampU32(cfg.adcISamples, 1, 64);
  cfg.adcDummy = (uint16_t)clampU32(cfg.adcDummy, 0, 8);

  if (!isfinite(cfg.adcRefV) || cfg.adcRefV < 1.0f || cfg.adcRefV > 3.6f) cfg.adcRefV = DEFAULT_ADC_REF_V;
  if (!isfinite(cfg.prechargeReadyV) || cfg.prechargeReadyV < 0.0f || cfg.prechargeReadyV > SEC_V_MAX_HARD) cfg.prechargeReadyV = DEFAULT_PRECHARGE_READY_V;
  if (!isfinite(cfg.vpriTopK) || cfg.vpriTopK < 1.0f || cfg.vpriTopK > 10000.0f) cfg.vpriTopK = DEFAULT_VPRI_TOP_K;
  if (!isfinite(cfg.vpriBottomK) || cfg.vpriBottomK < 0.1f || cfg.vpriBottomK > 1000.0f) cfg.vpriBottomK = DEFAULT_VPRI_BOTTOM_K;
  if (!isfinite(cfg.vpriGain) || cfg.vpriGain < 0.1f || cfg.vpriGain > 10.0f) cfg.vpriGain = 1.0f;
  if (!isfinite(cfg.vpriOffsetV) || cfg.vpriOffsetV < -100.0f || cfg.vpriOffsetV > 100.0f) cfg.vpriOffsetV = 0.0f;

  if (!isfinite(cfg.amcRefV) || cfg.amcRefV < 1.0f || cfg.amcRefV > 5.0f) cfg.amcRefV = DEFAULT_AMC_REFIN_V;
  if (!isfinite(cfg.amcVclipV) || cfg.amcVclipV < 0.5f || cfg.amcVclipV > 3.0f) cfg.amcVclipV = DEFAULT_AMC_VCLIP_V;
  if (!isfinite(cfg.vsecTopK) || cfg.vsecTopK < 1.0f || cfg.vsecTopK > 10000.0f) cfg.vsecTopK = DEFAULT_VSEC_TOP_K;
  if (!isfinite(cfg.vsecBottomK) || cfg.vsecBottomK < 0.1f || cfg.vsecBottomK > 1000.0f) cfg.vsecBottomK = DEFAULT_VSEC_BOTTOM_K;
  if (!isfinite(cfg.vsecGain) || cfg.vsecGain < 0.1f || cfg.vsecGain > 10.0f) cfg.vsecGain = 1.0f;
  if (!isfinite(cfg.vsecOffsetV) || cfg.vsecOffsetV < -20.0f || cfg.vsecOffsetV > 20.0f) cfg.vsecOffsetV = 0.0f;

  if (!isfinite(cfg.csResOhms) || cfg.csResOhms < 1.0f || cfg.csResOhms > 10000.0f) cfg.csResOhms = DEFAULT_CS_RES_OHMS;
  if (!isfinite(cfg.csGainAperA) || cfg.csGainAperA < 0.000001f || cfg.csGainAperA > 0.1f) cfg.csGainAperA = DEFAULT_CS_GAIN_A_PER_A;
  if (!isfinite(cfg.currentOffsetV) || cfg.currentOffsetV < -1.0f || cfg.currentOffsetV > 1.0f) cfg.currentOffsetV = 0.0f;
  if (!isfinite(cfg.currentTripA) || cfg.currentTripA < 0.1f || cfg.currentTripA > 100.0f) cfg.currentTripA = DEFAULT_CURRENT_TRIP_A;
  if (!isfinite(cfg.currentSoftA) || cfg.currentSoftA < 0.0f || cfg.currentSoftA > 100.0f) cfg.currentSoftA = DEFAULT_CURRENT_SOFT_A;
  if (!isfinite(cfg.currentFoldPctPerA) || cfg.currentFoldPctPerA < 0.0f || cfg.currentFoldPctPerA > 100.0f) cfg.currentFoldPctPerA = DEFAULT_CURRENT_FOLD_PCT_A;
  cfg.currentTripEnable = cfg.currentTripEnable ? 1 : 0;
  cfg.currentFoldbackEnable = cfg.currentFoldbackEnable ? 1 : 0;

  if (!isfinite(cfg.targetPowerW) || cfg.targetPowerW < POWER_TARGET_MIN_W || cfg.targetPowerW > POWER_TARGET_MAX_W) cfg.targetPowerW = DEFAULT_POWER_TARGET_W;
  cfg.kp_x1000 = clampI32(cfg.kp_x1000, 0, 50000);
  cfg.ki_x1000 = clampI32(cfg.ki_x1000, 0, 200000);
  cfg.deadbandMw = clampI32(cfg.deadbandMw, 0, 100000);
  cfg.slewX10PerSec = clampI32(cfg.slewX10PerSec, 1, 30000);
  cfg.integralMinX10 = clampI32(cfg.integralMinX10, -1000, 1000);
  cfg.integralMaxX10 = clampI32(cfg.integralMaxX10, -1000, 1000);
  if (cfg.integralMaxX10 < cfg.integralMinX10) cfg.integralMaxX10 = cfg.integralMinX10;

  if (!isfinite(cfg.powerTauMs) || cfg.powerTauMs < 0.1f || cfg.powerTauMs > 500.0f) cfg.powerTauMs = DEFAULT_POWER_TAU_MS;
  if (!isfinite(cfg.vpriTauMs) || cfg.vpriTauMs < 0.1f || cfg.vpriTauMs > 500.0f) cfg.vpriTauMs = DEFAULT_VPRI_TAU_MS;
  if (!isfinite(cfg.currentTauMs) || cfg.currentTauMs < 0.1f || cfg.currentTauMs > 500.0f) cfg.currentTauMs = DEFAULT_CURRENT_TAU_MS;
  if (!isfinite(cfg.vsecTauMs) || cfg.vsecTauMs < 0.1f || cfg.vsecTauMs > 500.0f) cfg.vsecTauMs = DEFAULT_VSEC_TAU_MS;

  cfg.secOvpEnable = cfg.secOvpEnable ? 1 : 0;
  if (!isfinite(cfg.secMinV) || cfg.secMinV < SEC_V_MIN_HARD || cfg.secMinV > SEC_V_MAX_HARD) cfg.secMinV = DEFAULT_SEC_MIN_V;
  if (!isfinite(cfg.secMaxV) || cfg.secMaxV < cfg.secMinV + 0.5f || cfg.secMaxV > SEC_V_MAX_HARD) cfg.secMaxV = DEFAULT_SEC_MAX_V;
  if (!isfinite(cfg.secOvpV) || cfg.secOvpV < cfg.secMaxV || cfg.secOvpV > SEC_V_MAX_HARD) cfg.secOvpV = DEFAULT_SEC_OVP_V;
  if (!isfinite(cfg.secLowBoostPctPerV) || cfg.secLowBoostPctPerV < 0.0f || cfg.secLowBoostPctPerV > 100.0f) cfg.secLowBoostPctPerV = DEFAULT_SEC_LOW_BOOST_PCT_V;
  if (!isfinite(cfg.secHighFoldPctPerV) || cfg.secHighFoldPctPerV < 0.0f || cfg.secHighFoldPctPerV > 100.0f) cfg.secHighFoldPctPerV = DEFAULT_SEC_HIGH_FOLD_PCT_V;

  cfg.maxDutyFaultEnable = cfg.maxDutyFaultEnable ? 1 : 0;
  cfg.maxDutyFaultErrMw = clampI32(cfg.maxDutyFaultErrMw, 0, 1000000);
  cfg.bangHystMw = clampI32(cfg.bangHystMw, 0, 1000000);

  cfg.autotuneMaxDutyX10 = clampDutyX10(cfg.autotuneMaxDutyX10);
  if (cfg.autotuneMaxDutyX10 > cfg.dutyMaxX10) cfg.autotuneMaxDutyX10 = cfg.dutyMaxX10;
  cfg.autotuneCoarseStepX10 = (uint16_t)clampU32(cfg.autotuneCoarseStepX10, 5, 250);
  cfg.autotuneFineStepX10 = (uint16_t)clampU32(cfg.autotuneFineStepX10, 1, 100);
  cfg.autotuneTestStepX10 = (uint16_t)clampU32(cfg.autotuneTestStepX10, 5, 150);
  cfg.autotuneSettleMs = clampU32(cfg.autotuneSettleMs, 20, 3000);
  cfg.autotuneMeasureMs = clampU32(cfg.autotuneMeasureMs, 20, 2000);
  cfg.autotuneFreqStepHz = clampU32(cfg.autotuneFreqStepHz, 500UL, 10000UL);
  if (!isfinite(cfg.enFreqPenaltyW) || cfg.enFreqPenaltyW < 0.0f || cfg.enFreqPenaltyW > 1000.0f) cfg.enFreqPenaltyW = DEFAULT_EN_FREQ_PENALTY_W;

  if (cfg.activeCalLoadSlot >= CAL_LOAD_SLOT_COUNT) cfg.activeCalLoadSlot = 0;
  for (uint8_t i = 0; i < CAL_LOAD_SLOT_COUNT; i++) {
    if (!isfinite(cfg.calLoadOhms[i]) || cfg.calLoadOhms[i] < 0.0f || cfg.calLoadOhms[i] > 100000.0f) cfg.calLoadOhms[i] = 0.0f;
    cfg.calLoadFreqHz[i] = clampU32(cfg.calLoadFreqHz[i], EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
    cfg.calLoadDutyX10[i] = clampDutyX10(cfg.calLoadDutyX10[i]);
    cfg.calLoadKp_x1000[i] = clampI32(cfg.calLoadKp_x1000[i], 0, 50000);
    cfg.calLoadKi_x1000[i] = clampI32(cfg.calLoadKi_x1000[i], 0, 200000);
    if (!isfinite(cfg.calLoadGainWPerPct[i]) || cfg.calLoadGainWPerPct[i] < 0.0f || cfg.calLoadGainWPerPct[i] > 1000.0f) cfg.calLoadGainWPerPct[i] = 0.0f;
    if (!isfinite(cfg.calLoadTauS[i]) || cfg.calLoadTauS[i] < 0.0f || cfg.calLoadTauS[i] > 20.0f) cfg.calLoadTauS[i] = 0.0f;
    if (!isfinite(cfg.calLoadTargetW[i]) || cfg.calLoadTargetW[i] < 0.0f || cfg.calLoadTargetW[i] > POWER_TARGET_MAX_W) cfg.calLoadTargetW[i] = 0.0f;
    if (!isfinite(cfg.calLoadMeasuredW[i]) || cfg.calLoadMeasuredW[i] < 0.0f || cfg.calLoadMeasuredW[i] > POWER_TARGET_MAX_W * 2.0f) cfg.calLoadMeasuredW[i] = 0.0f;
    if (!isfinite(cfg.calLoadMeasuredVsec[i]) || cfg.calLoadMeasuredVsec[i] < -5.0f || cfg.calLoadMeasuredVsec[i] > 100.0f) cfg.calLoadMeasuredVsec[i] = 0.0f;
    if (!isfinite(cfg.calLoadMeasuredI[i]) || cfg.calLoadMeasuredI[i] < 0.0f || cfg.calLoadMeasuredI[i] > 100.0f) cfg.calLoadMeasuredI[i] = 0.0f;
  }

  if (!isfinite(cfg.tunedPlantGainWPerPct) || cfg.tunedPlantGainWPerPct < 0.0f || cfg.tunedPlantGainWPerPct > 1000.0f) cfg.tunedPlantGainWPerPct = 0.0f;
  if (!isfinite(cfg.tunedPlantTauS) || cfg.tunedPlantTauS < 0.0f || cfg.tunedPlantTauS > 20.0f) cfg.tunedPlantTauS = 0.0f;
  cfg.tunedDutyX10 = clampDutyX10(cfg.tunedDutyX10);
  if (!isfinite(cfg.tunedTargetW) || cfg.tunedTargetW < 0.0f || cfg.tunedTargetW > POWER_TARGET_MAX_W) cfg.tunedTargetW = 0.0f;

  controlMode = (ControlMode)cfg.controlMode;
  systemEnabled = cfg.systemEnabled ? true : false;
}

uint32_t checksumSettings(const SettingsSlot &s) {
  const uint8_t *p = (const uint8_t *)&s;
  uint32_t sum = 0xA5A55A5AUL;
  for (size_t i = 0; i < sizeof(SettingsSlot) - sizeof(uint32_t); i++) {
    sum = (sum << 5) | (sum >> 27);
    sum ^= p[i];
  }
  return sum;
}

void eepromReadBytes(int addr, uint8_t *dst, size_t len) {
  for (size_t i = 0; i < len; i++) dst[i] = EEPROM.read(addr + (int)i);
}

void eepromWriteBytes(int addr, const uint8_t *src, size_t len) {
  for (size_t i = 0; i < len; i++) EEPROM.update(addr + (int)i, src[i]);
}

int slotAddress(int slot) {
  return EEPROM_BASE_ADDR + slot * (int)sizeof(SettingsSlot);
}

bool readSlot(int slot, SettingsSlot &s) {
  eepromReadBytes(slotAddress(slot), (uint8_t *)&s, sizeof(SettingsSlot));
  if (s.magic != EEPROM_MAGIC) return false;
  if (s.checksum != checksumSettings(s)) return false;
  return true;
}

void loadSettings() {
  SettingsSlot best;
  bool found = false;
  uint32_t bestSeq = 0;

  for (int i = 0; i < EEPROM_SLOT_COUNT; i++) {
    SettingsSlot s;
    if (readSlot(i, s)) {
      if (!found || s.sequence > bestSeq) {
        found = true;
        bestSeq = s.sequence;
        best = s;
        activeSlotIndex = i;
      }
    }
  }

  if (found) {
    cfg = best;
    settingsSequence = bestSeq;
  } else {
    setDefaults();
    settingsSequence = 0;
    activeSlotIndex = -1;
  }
  validateSettings();
}

bool safeToWriteEepromNow() {
  return !systemEnabled && !autoTuneRunning && !startupPrechargeActive();
}

void markSettingsDirty() {
  settingsDirty = true;
  settingsDirtyMs = millis();
}

void saveSettingsNow() {
  cfg.magic = EEPROM_MAGIC;
  cfg.systemEnabled = systemEnabled ? 1 : 0;
  cfg.controlMode = (uint8_t)controlMode;
  validateSettings();

  cfg.magic = EEPROM_MAGIC;
  cfg.sequence = settingsSequence + 1;
  cfg.systemEnabled = systemEnabled ? 1 : 0;
  cfg.controlMode = (uint8_t)controlMode;
  cfg.checksum = checksumSettings(cfg);

  int nextSlot = (activeSlotIndex + 1) % EEPROM_SLOT_COUNT;
  if (activeSlotIndex < 0) nextSlot = 0;
  eepromWriteBytes(slotAddress(nextSlot), (const uint8_t *)&cfg, sizeof(SettingsSlot));
  settingsSequence = cfg.sequence;
  activeSlotIndex = nextSlot;
  settingsDirty = false;
  settingsDirtyMs = 0;
}

bool requestSettingsSave(const char *reason) {
  (void)reason;
  if (safeToWriteEepromNow()) {
    saveSettingsNow();
    return true;
  }
  markSettingsDirty();
  return false;
}

void saveSettings() {
  (void)requestSettingsSave(nullptr);
}

bool flushPendingSettingsSave(bool quiet) {
  if (!settingsDirty) return true;
  if (!safeToWriteEepromNow()) return false;
  if (!quiet) CmdSerial.println("Saving pending settings to EEPROM...");
  saveSettingsNow();
  if (!quiet) CmdSerial.println("Saved.");
  return true;
}

// ============================================================
// PA10 EN timing using TIM3 fixed-period update/compare
// ============================================================

void setPA10High() { GPIOA->BSRR = (1UL << 10); }
void setPA10Low()  { GPIOA->BSRR = (1UL << (10 + 16)); }

void setGateCarrierDrive(bool enable) {
  (void)enable;
  TIM1->BDTR |= (1UL << 15);
  enSyncCarrierActive = true;
}

uint32_t gateCyclesToUsCeil(uint32_t cycles) {
  if (cycles == 0) return 0;
  return (uint32_t)(((uint64_t)cycles * 1000000ULL + GATE_FREQ_HZ - 1ULL) / GATE_FREQ_HZ);
}

uint16_t gateCyclesFromUsCeil(uint32_t us) {
  if (us == 0) return 0;
  uint64_t cycles = ((uint64_t)us * (uint64_t)GATE_FREQ_HZ + 999999ULL) / 1000000ULL;
  if (cycles < 1ULL) cycles = 1ULL;
  if (cycles > 65535ULL) cycles = 65535ULL;
  return (uint16_t)cycles;
}

uint16_t leadGateCycles() {
  return (uint16_t)clampU32(cfg.enGateLeadCycles, EN_GATE_LEAD_CYCLES_MIN, EN_GATE_LEAD_CYCLES_MAX);
}

uint32_t leadGateUs() {
  return gateCyclesToUsCeil(leadGateCycles());
}

void setTim1CarrierSyncIrq(bool enable) {
#if defined(TIM1_BRK_UP_TRG_COM_IRQn)
  if (enable) {
    TIM1->SR &= ~TIM_SR_UIF;
    TIM1->DIER |= TIM_DIER_UIE;
    NVIC_EnableIRQ(TIM1_BRK_UP_TRG_COM_IRQn);
  } else {
    TIM1->DIER &= ~TIM_DIER_UIE;
  }
#else
  (void)enable;
#endif
}

void forceEnSyncLowNow() {
  setGateCarrierDrive(true);
  setPA10Low();
  enSyncBurstPending = false;
  enSyncLeadCyclesLeft = 0;
  enSyncDriveCyclesLeft = 0;
  enSyncTailCyclesLeft = 0;
  enPwmStateHigh = false;
  setTim1CarrierSyncIrq(false);
}

void requestCarrierSyncedBurst(uint16_t driveCycles) {
  if (driveCycles < EN_MIN_GATE_CYCLES_MIN) driveCycles = EN_MIN_GATE_CYCLES_MIN;
  enSyncRequestedDriveCycles = driveCycles;
  enSyncBurstPending = true;
  setTim1CarrierSyncIrq(true);
}

uint32_t clampEnFreq(uint32_t hz) {
  return clampU32(hz, cfg.enFreqMinHz, cfg.enFreqMaxHz);
}

uint16_t clampControlDutyLimit(uint16_t dutyX10) {
  if (dutyX10 < cfg.dutyMinX10) dutyX10 = cfg.dutyMinX10;
  if (dutyX10 > cfg.dutyMaxX10) dutyX10 = cfg.dutyMaxX10;
  return dutyX10;
}

uint32_t minCompleteGateBurstUs() {
  uint32_t cycles = clampU32(cfg.enMinGateCycles, EN_MIN_GATE_CYCLES_MIN, EN_MIN_GATE_CYCLES_MAX);
  return gateCyclesToUsCeil(cycles);
}

void updateEnableTimingNoInterruptLock() {
  uint32_t f = clampEnFreq(enFreqRuntimeHz);
  enFreqRuntimeHz = f;

  uint32_t period = (1000000UL + (f / 2UL)) / f;
  uint32_t minLow = clampU32(cfg.enMinEdgeUs, EN_MIN_EDGE_HARD_US, EN_MAX_EDGE_HARD_US);
  uint32_t minDrive = minCompleteGateBurstUs();
  uint32_t leadUsNow = leadGateUs();
  uint32_t tailUsNow = gateCyclesToUsCeil(EN_GATE_TAIL_CYCLES);
  uint32_t minEnvelope = leadUsNow + minDrive + tailUsNow;
  if (period < minEnvelope + minLow) period = minEnvelope + minLow;

  uint16_t rawCmd = enDutyCmdX10;
  uint16_t cmd = rawCmd;
  if (rawCmd != 0 && !enDutyLimitBypass) cmd = clampControlDutyLimit(cmd);

  uint32_t high = ((uint64_t)period * (uint64_t)cmd + 500ULL) / 1000ULL;
  uint16_t pulseSkip = 1;
  if (rawCmd == 0 || cmd == 0) high = 0;
  else if (cmd >= 1000 && cfg.allowStatic100) high = period;
  else {
    if (high < minDrive) high = minDrive;
    uint64_t requestedHighX1000 = (uint64_t)period * (uint64_t)cmd;
    if (requestedHighX1000 > 0ULL && requestedHighX1000 < (uint64_t)minDrive * 1000ULL) {
      uint64_t skip = (((uint64_t)minDrive * 1000ULL) + requestedHighX1000 - 1ULL) / requestedHighX1000;
      if (skip < 1ULL) skip = 1ULL;
      if (skip > 60000ULL) skip = 60000ULL;
      pulseSkip = (uint16_t)skip;
    }
    uint32_t maxDrive = (period > leadUsNow + tailUsNow + minLow) ? (period - leadUsNow - tailUsNow - minLow) : minDrive;
    if (high > maxDrive) high = maxDrive;
  }

  enPeriodUs = period;
  enHighUs = high;
  enHighGateCycles = gateCyclesFromUsCeil(high);
  if (high != 0 && enHighGateCycles < cfg.enMinGateCycles) enHighGateCycles = cfg.enMinGateCycles;
  if (pulseSkip != enPulseSkipN || high == 0) enPulseSkipCountdown = 0;
  enPulseSkipN = pulseSkip;

  uint32_t averagePeriod = period * (uint32_t)pulseSkip;
  enDutyEffX10 = (averagePeriod == 0) ? 0 : (uint16_t)(((uint64_t)1000UL * (uint64_t)high + averagePeriod / 2UL) / averagePeriod);
}

uint32_t enCompareUsForTimer() {
  uint32_t period = enPeriodUs;
  if (period < 2UL) period = 2UL;
  if (enHighUs == 0 || enHighUs >= period) return period - 1UL;
  return enHighUs;
}

void applyEnableTimerNoInterruptLock(bool periodChanged) {
  if (EnTimer == nullptr) return;
  if (periodChanged) EnTimer->setOverflow(enPeriodUs, MICROSEC_FORMAT);
  EnTimer->setCaptureCompare(1, enCompareUsForTimer(), MICROSEC_COMPARE_FORMAT);
  enTimerAppliedHighUs = enHighUs;
  enTimerAppliedPulseSkipN = enPulseSkipN;
}

void enPeriodISR() {
  if (!systemEnabled || faultLatched || enHighUs == 0 || enDutyEffX10 == 0) {
    forceEnSyncLowNow();
    return;
  }

  if (enPulseSkipN > 1) {
    if (enPulseSkipCountdown == 0) {
      enPulseSkipCountdown = enPulseSkipN - 1;
    } else {
      enPulseSkipCountdown--;
      forceEnSyncLowNow();
      return;
    }
  }

  requestCarrierSyncedBurst(enHighGateCycles);
}

void enCompareISR() {
  if (!systemEnabled || faultLatched || enHighUs == 0 || enDutyEffX10 == 0) {
    forceEnSyncLowNow();
    return;
  }
  // Normal turn-off is handled by the TIM1 carrier update ISR so PA10
  // never cuts a half-bridge cycle short.
}

void handleTim1CarrierSyncUpdate() {
  if (!systemEnabled || faultLatched || enHighUs == 0 || enDutyEffX10 == 0) {
    if (enPwmStateHigh || enSyncBurstPending || enSyncCarrierActive) enSyncAbortCount++;
    forceEnSyncLowNow();
    return;
  }

  if (enSyncBurstPending && !enPwmStateHigh) {
    enSyncBurstPending = false;
    enSyncLeadCyclesLeft = leadGateCycles();
    enSyncDriveCyclesLeft = enSyncRequestedDriveCycles;
    enSyncTailCyclesLeft = (uint16_t)EN_GATE_TAIL_CYCLES;
    setGateCarrierDrive(true);
    setPA10High();
    enPwmStateHigh = true;
    enSyncRiseCount++;
    if (enSyncLeadCyclesLeft == 0) enSyncDriveStartCount++;
    return;
  }

  if (!enPwmStateHigh) {
    if (!enSyncBurstPending) setTim1CarrierSyncIrq(false);
    return;
  }

  if (enSyncLeadCyclesLeft > 0) {
    enSyncLeadCyclesLeft--;
    if (enSyncLeadCyclesLeft > 0) return;
    enSyncDriveStartCount++;
    return;
  }

  if (!enSyncCarrierActive) {
    setGateCarrierDrive(true);
    enSyncDriveStartCount++;
    return;
  }

  if (enSyncDriveCyclesLeft > 0) {
    enSyncDriveCyclesLeft--;
    if (enSyncDriveCyclesLeft > 0) return;
  }

  if (enSyncTailCyclesLeft > 0) {
    enSyncTailCyclesLeft--;
    if (enSyncTailCyclesLeft > 0) return;
  }

  setPA10Low();
  enPwmStateHigh = false;
  enSyncFallCount++;
  if (!enSyncBurstPending) setTim1CarrierSyncIrq(false);
}

#if defined(TIM1_BRK_UP_TRG_COM_IRQn)
extern "C" void TIM1_BRK_UP_TRG_COM_IRQHandler(void) {
  if (TIM1->SR & TIM_SR_UIF) {
    TIM1->SR &= ~TIM_SR_UIF;
    handleTim1CarrierSyncUpdate();
  }
}
#endif

void setupEnablePWM() {
  pinMode(EN_PIN, OUTPUT);
  setPA10Low();
  noInterrupts();
  enFreqRuntimeHz = cfg.enFreqHz;
  enDutyCmdX10 = cfg.openLoopDutyX10;
  updateEnableTimingNoInterruptLock();
  interrupts();

  EnTimer->pause();
  EnTimer->setInterruptPriority(0, 0);
  EnTimer->setMode(1, TIMER_DISABLED);
  EnTimer->setOverflow(enPeriodUs, MICROSEC_FORMAT);
  EnTimer->setCaptureCompare(1, enCompareUsForTimer(), MICROSEC_COMPARE_FORMAT);
  EnTimer->attachInterrupt(enPeriodISR);
  EnTimer->attachInterrupt(1, enCompareISR);
  EnTimer->refresh();
  EnTimer->resume();
}

void setEnFrequencyHz(uint32_t hz) {
  hz = clampEnFreq(hz);
  noInterrupts();
  enFreqRuntimeHz = hz;
  cfg.enFreqHz = hz;
  updateEnableTimingNoInterruptLock();
  enPulseSkipCountdown = 0;
  applyEnableTimerNoInterruptLock(true);
  interrupts();
}

void applyEnDutyCommand(uint16_t dutyX10, bool bypassLimits) {
  noInterrupts();
  uint16_t oldDuty = enDutyCmdX10;
  bool oldBypass = enDutyLimitBypass;
  enDutyLimitBypass = bypassLimits;
  enDutyCmdX10 = clampDutyX10(dutyX10);
  updateEnableTimingNoInterruptLock();
  if (oldDuty != enDutyCmdX10 || oldBypass != enDutyLimitBypass) enPulseSkipCountdown = 0;
  if (enHighUs != enTimerAppliedHighUs || enPulseSkipN != enTimerAppliedPulseSkipN) applyEnableTimerNoInterruptLock(false);
  if (enHighUs == 0 || !systemEnabled || faultLatched) {
    forceEnSyncLowNow();
  }
  interrupts();
}

void setEnDutyX10(uint16_t dutyX10) {
  applyEnDutyCommand(dutyX10, false);
}

void setEnDutyX10BypassLimits(uint16_t dutyX10) {
  applyEnDutyCommand(dutyX10, true);
}

float getCmdDutyPercent() { return dutyX10ToPercent(enDutyCmdX10); }
float getEffDutyPercent() { return dutyX10ToPercent(enDutyEffX10); }

// ============================================================
// TIM1 PA8 / PA9 fixed carrier
// ============================================================

void setupPA8PA9_TIM1_AF2() {
#if defined(GPIO_MODER_MODE8_Msk)
  GPIOA->MODER &= ~((3UL << (8 * 2)) | (3UL << (9 * 2)));
  GPIOA->MODER |=  ((2UL << (8 * 2)) | (2UL << (9 * 2)));
  GPIOA->AFR[1] &= ~((0xFUL << ((8 - 8) * 4)) | (0xFUL << ((9 - 8) * 4)));
  GPIOA->AFR[1] |=  ((2UL << ((8 - 8) * 4)) | (2UL << ((9 - 8) * 4)));
#endif
}

bool calculateGateTiming(uint32_t &arr, uint32_t &ccr1, uint32_t &ccr2,
                         uint32_t &deadTicks, uint32_t &actualDeadNs) {
  uint32_t timClk = HAL_RCC_GetPCLK1Freq();
#if defined(RCC_CFGR_PPRE_Msk)
  if ((RCC->CFGR & RCC_CFGR_PPRE_Msk) != 0) timClk *= 2UL;
#endif
  if (timClk < GATE_FREQ_HZ * 4UL) return false;

  uint32_t ticks = (timClk + GATE_FREQ_HZ / 2UL) / GATE_FREQ_HZ;
  if (ticks < 8) return false;

  arr = ticks - 1UL;
  deadTicks = (uint32_t)(((uint64_t)GATE_DEADTIME_NS * (uint64_t)timClk + 500000000ULL) / 1000000000ULL);
  if (deadTicks < 1) deadTicks = 1;
  if (deadTicks >= ticks / 2UL) return false;

  uint32_t center = ticks / 2UL;
  uint32_t left = deadTicks / 2UL;
  uint32_t right = deadTicks - left;
  ccr1 = center - left;
  ccr2 = center + right;
  if (ccr1 == 0 || ccr2 >= ticks || ccr2 <= ccr1) return false;

  actualDeadNs = (uint32_t)(((uint64_t)(ccr2 - ccr1) * 1000000000ULL) / (uint64_t)timClk);
  return true;
}

void setupGatePWM() {
  setupPA8PA9_TIM1_AF2();
#if defined(RCC_APBENR2_TIM1EN)
  RCC->APBENR2 |= RCC_APBENR2_TIM1EN;
#elif defined(RCC_APB2ENR_TIM1EN)
  RCC->APB2ENR |= RCC_APB2ENR_TIM1EN;
#endif

  TIM1->CR1 = 0;
  TIM1->CR2 = 0;
  TIM1->SMCR = 0;
  TIM1->DIER = 0;
  TIM1->PSC = 0;
  TIM1->CNT = 0;

  TIM1->CCMR1 = 0;
  TIM1->CCMR1 |= (6UL << 4);   // CH1 PWM mode 1
  TIM1->CCMR1 |= (1UL << 3);   // CH1 preload
  TIM1->CCMR1 |= (7UL << 12);  // CH2 PWM mode 2
  TIM1->CCMR1 |= (1UL << 11);  // CH2 preload

  TIM1->CCER = 0;
  TIM1->CCER |= (1UL << 0); // CH1 enable
  TIM1->CCER |= (1UL << 4); // CH2 enable
  TIM1->BDTR = 0;
  TIM1->BDTR |= (1UL << 10); // OSSI: keep outputs in idle state when MOE is off
  TIM1->BDTR |= (1UL << 11); // OSSR: keep outputs in idle state during run-mode off state

  uint32_t arr, ccr1, ccr2, deadTicks, actualDeadNs;
  if (!calculateGateTiming(arr, ccr1, ccr2, deadTicks, actualDeadNs)) {
    CmdSerial.println("ERROR: TIM1 fixed gate timing invalid.");
    return;
  }

  TIM1->ARR = arr;
  TIM1->CCR1 = ccr1;
  TIM1->CCR2 = ccr2;
  TIM1->EGR = 1;
  TIM1->CR1 |= (1UL << 7);   // ARPE
  TIM1->CR1 |= 1UL;          // CEN
  setGateCarrierDrive(true);
  setTim1CarrierSyncIrq(false);
#if defined(TIM1_BRK_UP_TRG_COM_IRQn)
  NVIC_SetPriority(TIM1_BRK_UP_TRG_COM_IRQn, 0);
  NVIC_EnableIRQ(TIM1_BRK_UP_TRG_COM_IRQn);
#endif

  CmdSerial.print("TIM1 PA8/PA9 fixed ");
  CmdSerial.print(GATE_FREQ_HZ);
  CmdSerial.print(" Hz, dead-time approx ");
  CmdSerial.print(actualDeadNs);
  CmdSerial.println(" ns");
}

void setGateOutputsEnabled(bool enable) {
#if KEEP_GATE_PWM_RUNNING
  TIM1->CR1 |= 1UL;
  if (!enable) {
    forceEnSyncLowNow();
  } else {
    setGateCarrierDrive(true);
  }
#else
  if (enable) {
    TIM1->CR1 |= 1UL;
    setGateCarrierDrive(true);
  } else {
    forceEnSyncLowNow();
  }
#endif
}

// ============================================================
// ADC / scaling
// ============================================================

bool configAdcDmaChannel(uint32_t channel, uint32_t rank) {
  ADC_ChannelConfTypeDef sConfig;
  memset(&sConfig, 0, sizeof(sConfig));
  sConfig.Channel = channel;
  sConfig.Rank = rank;
  sConfig.SamplingTime = ADC_SAMPLINGTIME_COMMON_1;
  return HAL_ADC_ConfigChannel(&adcDmaHandle, &sConfig) == HAL_OK;
}

bool setupAdcDma() {
  adcDmaRunning = false;

#if defined(__HAL_RCC_ADC_CLK_ENABLE)
  __HAL_RCC_ADC_CLK_ENABLE();
#endif
#if defined(__HAL_RCC_DMA1_CLK_ENABLE)
  __HAL_RCC_DMA1_CLK_ENABLE();
#endif

  memset((void *)&adcDmaHandle, 0, sizeof(adcDmaHandle));
  memset((void *)&adcDmaHandleDma, 0, sizeof(adcDmaHandleDma));

  adcDmaHandle.Instance = ADC1;
  adcDmaHandle.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
  adcDmaHandle.Init.Resolution = ADC_RESOLUTION_12B;
  adcDmaHandle.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  adcDmaHandle.Init.ScanConvMode = ADC_SCAN_ENABLE;
  adcDmaHandle.Init.EOCSelection = ADC_EOC_SEQ_CONV;
  adcDmaHandle.Init.LowPowerAutoWait = DISABLE;
  adcDmaHandle.Init.LowPowerAutoPowerOff = DISABLE;
  adcDmaHandle.Init.ContinuousConvMode = ENABLE;
  adcDmaHandle.Init.NbrOfConversion = ADC_DMA_CHANNEL_COUNT;
  adcDmaHandle.Init.DiscontinuousConvMode = DISABLE;
  adcDmaHandle.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  adcDmaHandle.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  adcDmaHandle.Init.DMAContinuousRequests = ENABLE;
  adcDmaHandle.Init.Overrun = ADC_OVR_DATA_OVERWRITTEN;
  adcDmaHandle.Init.SamplingTimeCommon1 = ADC_SAMPLETIME_39CYCLES_5;
  adcDmaHandle.Init.SamplingTimeCommon2 = ADC_SAMPLETIME_39CYCLES_5;
  adcDmaHandle.Init.OversamplingMode = DISABLE;

  adcDmaHandleDma.Instance = DMA1_Channel1;
  adcDmaHandleDma.Init.Request = DMA_REQUEST_ADC1;
  adcDmaHandleDma.Init.Direction = DMA_PERIPH_TO_MEMORY;
  adcDmaHandleDma.Init.PeriphInc = DMA_PINC_DISABLE;
  adcDmaHandleDma.Init.MemInc = DMA_MINC_ENABLE;
  adcDmaHandleDma.Init.PeriphDataAlignment = DMA_PDATAALIGN_HALFWORD;
  adcDmaHandleDma.Init.MemDataAlignment = DMA_MDATAALIGN_HALFWORD;
  adcDmaHandleDma.Init.Mode = DMA_CIRCULAR;
  adcDmaHandleDma.Init.Priority = DMA_PRIORITY_HIGH;

  if (HAL_DMA_Init(&adcDmaHandleDma) != HAL_OK) {
    adcDmaStartErrors++;
    return false;
  }
  __HAL_LINKDMA(&adcDmaHandle, DMA_Handle, adcDmaHandleDma);

  if (HAL_ADC_Init(&adcDmaHandle) != HAL_OK) {
    adcDmaStartErrors++;
    return false;
  }
  if (!configAdcDmaChannel(ADC_CHANNEL_0, ADC_REGULAR_RANK_1)) { adcDmaStartErrors++; return false; }
  if (!configAdcDmaChannel(ADC_CHANNEL_1, ADC_REGULAR_RANK_2)) { adcDmaStartErrors++; return false; }
  if (!configAdcDmaChannel(ADC_CHANNEL_2, ADC_REGULAR_RANK_3)) { adcDmaStartErrors++; return false; }

  (void)HAL_ADCEx_Calibration_Start(&adcDmaHandle);

  if (HAL_ADC_Start_DMA(&adcDmaHandle, (uint32_t *)adcDmaBuffer, ADC_DMA_CHANNEL_COUNT) != HAL_OK) {
    adcDmaStartErrors++;
    return false;
  }

  adcDmaRunning = true;
  return true;
}

uint16_t readAdcDmaChannel(uint8_t index) {
  if (index >= ADC_DMA_CHANNEL_COUNT) return 0;
  return (uint16_t)(adcDmaBuffer[index] & ADC_MAX_COUNTS);
}

float adcCountsToVoltage(uint16_t counts) {
  return ((float)counts * cfg.adcRefV) / (float)ADC_MAX_COUNTS;
}

float dividerRatio(float topK, float bottomK) {
  if (topK <= 0.0f || bottomK <= 0.0f) return 1.0f;
  return bottomK / (topK + bottomK);
}

float readPrimaryVoltageRaw() {
  rawPa0Adc = readAdcDmaChannel(ADC_DMA_VPRI_INDEX);
  rawPa0Voltage = adcCountsToVoltage(rawPa0Adc);
  float ratio = dividerRatio(cfg.vpriTopK, cfg.vpriBottomK);
  if (ratio <= 0.0f) ratio = dividerRatio(DEFAULT_VPRI_TOP_K, DEFAULT_VPRI_BOTTOM_K);
  float v = (rawPa0Voltage / ratio) * cfg.vpriGain + cfg.vpriOffsetV;
  if (v < 0.0f && v > -2.0f) v = 0.0f;
  return v;
}

float amcOutputToInputVoltage(float amcOutV) {
  return ((amcOutV - (cfg.amcRefV * 0.5f)) * 2.0f * cfg.amcVclipV) / cfg.amcRefV;
}

float readSecondaryVoltageRaw() {
  rawPa1Adc = readAdcDmaChannel(ADC_DMA_VSEC_INDEX);
  rawPa1Voltage = adcCountsToVoltage(rawPa1Adc);
  float ratio = dividerRatio(cfg.vsecTopK, cfg.vsecBottomK);
  if (ratio <= 0.0f) ratio = dividerRatio(DEFAULT_VSEC_TOP_K, DEFAULT_VSEC_BOTTOM_K);
  float v = (amcOutputToInputVoltage(rawPa1Voltage) / ratio) * cfg.vsecGain + cfg.vsecOffsetV;
  if (v < 0.0f && v > -0.75f) v = 0.0f;
  return v;
}

float readPrimaryCurrentRaw() {
  rawPa2Adc = readAdcDmaChannel(ADC_DMA_I_INDEX);
  rawPa2Voltage = adcCountsToVoltage(rawPa2Adc);
  float denom = cfg.csResOhms * cfg.csGainAperA;
  if (denom <= 0.000001f) denom = DEFAULT_CS_RES_OHMS * DEFAULT_CS_GAIN_A_PER_A;
  float amps = (rawPa2Voltage - cfg.currentOffsetV) / denom;
  if (cfg.currentAbsMode) amps = fabsf(amps);
  if (amps < 0.0f) amps = 0.0f;
  return amps;
}

const char *powerFeedbackName() {
  if (cfg.powerFeedbackMode == PFB_SECONDARY_VI) return "SEC_V_I";
  return "PRI_V_I";
}

float computeFeedbackPower(float vpri, float vsec, float amps) {
  if (cfg.powerFeedbackMode == PFB_SECONDARY_VI) return vsec * amps;
  return vpri * amps;
}

bool feedbackMeasurementValid(float vpri, float vsec, float amps, float powerW) {
  if (amps < 0.0f || powerW < 0.0f) return false;
  if (cfg.powerFeedbackMode == PFB_SECONDARY_VI) return vsec > 0.2f;
  return vpri > 1.0f;
}

void updateAnalogFilters(bool readAll) {
  uint32_t blockStartUs = micros();
  float vpri = latestVpriRaw;
  float vsec = latestVsecRaw;
  float amps = latestCurrentRaw;

  if (readAll) {
    vpri = readPrimaryVoltageRaw();
    vsec = readSecondaryVoltageRaw();
    amps = readPrimaryCurrentRaw();
  }

  uint32_t blockUs = micros() - blockStartUs;
  lastAdcBlockUs = blockUs;
  if (blockUs > maxAdcBlockUs) maxAdcBlockUs = blockUs;

  float p = computeFeedbackPower(vpri, vsec, amps);
  uint32_t nowUs = micros();
  float dt = 0.001f;
  if (lastAnalogUs != 0) {
    dt = ((float)(nowUs - lastAnalogUs)) / 1000000.0f;
    dt = clampFloat(dt, 0.00002f, 0.5f);
  }
  lastAnalogUs = nowUs;

  latestVpriRaw = vpri;
  latestVsecRaw = vsec;
  latestCurrentRaw = amps;
  latestPowerRaw = p;

  if (!filtersPrimed) {
    filteredVpri = vpri;
    filteredVsec = vsec;
    filteredCurrent = amps;
    filteredPower = p;
    filtersPrimed = true;
    return;
  }

  float aVpri = dt / ((cfg.vpriTauMs / 1000.0f) + dt);
  float aVsec = dt / ((cfg.vsecTauMs / 1000.0f) + dt);
  float aI = dt / ((cfg.currentTauMs / 1000.0f) + dt);
  float aP = dt / ((cfg.powerTauMs / 1000.0f) + dt);
  filteredVpri += clampFloat(aVpri, 0.001f, 1.0f) * (vpri - filteredVpri);
  filteredVsec += clampFloat(aVsec, 0.001f, 1.0f) * (vsec - filteredVsec);
  filteredCurrent += clampFloat(aI, 0.001f, 1.0f) * (amps - filteredCurrent);
  filteredPower += clampFloat(aP, 0.001f, 1.0f) * (p - filteredPower);
}

// ============================================================
// Faults / mode
// ============================================================

const char *faultName() {
  switch (faultCode) {
    case FAULT_NONE: return "NONE";
    case FAULT_CURRENT: return "CURRENT";
    case FAULT_OVP: return "OVP";
    case FAULT_SENSOR: return "SENSOR";
    case FAULT_MAX_DUTY: return "MAX_DUTY";
    default: return "?";
  }
}

void latchFault(FaultCode code, const char *msg) {
  faultLatched = true;
  faultCode = code;
  setEnDutyX10(0);
  setGateOutputsEnabled(false);
  updateModeLEDs();
  CmdSerial.println();
  CmdSerial.print("FAULT: ");
  CmdSerial.println(msg);
  CmdSerial.println("Type CLR to clear.");
  CmdSerial.print("> ");
}

bool checkFaults() {
  if (faultLatched) return true;
  if (!adcDmaRunning) {
    latchFault(FAULT_SENSOR, "ADC DMA not running");
    return true;
  }
  if (cfg.currentTripEnable && filteredCurrent > cfg.currentTripA) {
    latchFault(FAULT_CURRENT, "primary current trip");
    return true;
  }
  if (cfg.secOvpEnable && filteredVsec > cfg.secOvpV) {
    latchFault(FAULT_OVP, "secondary over-voltage");
    return true;
  }
  return false;
}

const char *startupPhaseName() {
  switch (startupPhase) {
    case STARTUP_BURST: return "BURST";
    case STARTUP_SETTLE: return "SETTLE";
    default: return "IDLE";
  }
}

bool startupPrechargeActive() {
  return startupPhase != STARTUP_IDLE;
}

bool checkStartupCurrentFault() {
  updateAnalogFilters(true);
  if (cfg.currentTripEnable && filteredCurrent > cfg.currentTripA) {
    latchFault(FAULT_CURRENT, "startup precharge current trip");
    return true;
  }
  return false;
}

void applyPostStartupDuty() {
  startupPhase = STARTUP_IDLE;
  startupPhaseStartMs = 0;
  startupBurstCount = 0;
  powerIntegratorPct = 0.0f;
  maxDutyStartMs = 0;

  if (!systemEnabled || faultLatched) {
    setEnDutyX10(0);
    return;
  }

  if (controlMode == MODE_OPEN_LOOP) {
    controlDutyPercent = dutyX10ToPercent(cfg.openLoopDutyX10);
    setEnDutyX10(cfg.openLoopDutyX10);
  } else {
    bangBangHigh = false;
    bangBangLastSwitchMs = millis();
    controlDutyPercent = dutyX10ToPercent(cfg.bangLowDutyX10);
    setEnDutyX10(cfg.bangLowDutyX10);
  }
}

void startStartupBurst() {
  startupBurstCount++;
  startupPhase = STARTUP_BURST;
  startupPhaseStartMs = millis();
  setEnFrequencyHz(cfg.enFreqHz);
  setEnDutyX10BypassLimits(cfg.prechargeDutyX10);
}

bool beginStartupPrecharge() {
  startupPhase = STARTUP_IDLE;
  startupPhaseStartMs = 0;
  startupBurstCount = 0;

  if (!cfg.prechargeEnable || cfg.prechargeDutyX10 == 0 || cfg.prechargeBurstMs == 0) {
    applyPostStartupDuty();
    return false;
  }

  filtersPrimed = false;
  setGateOutputsEnabled(true);
  startStartupBurst();
  return true;
}

bool handleStartupPrecharge() {
  if (!startupPrechargeActive()) return false;

  if (!systemEnabled || faultLatched) {
    startupPhase = STARTUP_IDLE;
    setEnDutyX10(0);
    return true;
  }

  if (startupPhase == STARTUP_BURST) {
    if (checkStartupCurrentFault()) return true;
    if (millis() - startupPhaseStartMs >= cfg.prechargeBurstMs) {
      setEnDutyX10(0);
      filtersPrimed = false;
      startupPhase = STARTUP_SETTLE;
      startupPhaseStartMs = millis();
    }
    return true;
  }

  if (startupPhase == STARTUP_SETTLE) {
    if (checkStartupCurrentFault()) return true;
    if (millis() - startupPhaseStartMs < cfg.prechargeSettleMs) return true;

    updateAnalogFilters(true);
    if (checkFaults()) return true;

    bool feedbackReady = cfg.prechargeReadyV <= 0.0f || filteredVsec >= cfg.prechargeReadyV;
    if (feedbackReady || startupBurstCount >= cfg.prechargeMaxBursts) {
      applyPostStartupDuty();
      return true;
    }

    startStartupBurst();
    return true;
  }

  startupPhase = STARTUP_IDLE;
  return true;
}

bool runStartupPrechargeBlocking() {
  if (!beginStartupPrecharge()) return !faultLatched;
  CmdSerial.print("Startup precharge: ");
  CmdSerial.print(dutyX10ToPercent(cfg.prechargeDutyX10), 2);
  CmdSerial.print("% for ");
  CmdSerial.print(cfg.prechargeBurstMs);
  CmdSerial.print(" ms, settle ");
  CmdSerial.print(cfg.prechargeSettleMs);
  CmdSerial.println(" ms");

  while (systemEnabled && startupPrechargeActive() && !faultLatched) {
    handleStartupPrecharge();
    delay(1);
  }
  return !faultLatched;
}

bool runPrechargeTuneBurst(uint16_t dutyX10, uint32_t burstMs, float &vAfter, float &maxCurrent, bool &highStop) {
  vAfter = filteredVsec;
  maxCurrent = filteredCurrent;
  highStop = false;

  filtersPrimed = false;
  setEnFrequencyHz(cfg.enFreqHz);
  setEnDutyX10BypassLimits(dutyX10);

  uint32_t startMs = millis();
  while (millis() - startMs < burstMs) {
    updateAnalogFilters(true);
    if (filteredCurrent > maxCurrent) maxCurrent = filteredCurrent;
    if (checkFaults()) {
      setEnDutyX10(0);
      return false;
    }
    if (filteredVsec > cfg.secMaxV) {
      highStop = true;
      setEnDutyX10(0);
      break;
    }
    delay(1);
  }

  setEnDutyX10(0);

  uint32_t settleStartMs = millis();
  while (millis() - settleStartMs < cfg.prechargeSettleMs) {
    updateAnalogFilters(true);
    if (filteredCurrent > maxCurrent) maxCurrent = filteredCurrent;
    if (checkFaults()) return false;
    if (filteredVsec > cfg.secMaxV) highStop = true;
    delay(1);
  }

  updateAnalogFilters(true);
  if (filteredCurrent > maxCurrent) maxCurrent = filteredCurrent;
  vAfter = filteredVsec;
  if (vAfter > cfg.secMaxV) highStop = true;
  return true;
}

void savePrechargeTuneResult(uint16_t dutyX10, uint8_t bursts, float vAfter) {
  cfg.prechargeEnable = 1;
  cfg.prechargeDutyX10 = dutyX10;
  cfg.prechargeMaxBursts = bursts;
  validateSettings();
  systemEnabled = false;
  cfg.systemEnabled = 0;
  setEnDutyX10(0);
  saveSettings();

  CmdSerial.println();
  CmdSerial.println("AUTOPRE RESULT SELECTED");
  CmdSerial.print("PREDUTY="); CmdSerial.print(dutyX10ToPercent(cfg.prechargeDutyX10), 2);
  CmdSerial.print("% PREMS="); CmdSerial.print(cfg.prechargeBurstMs);
  CmdSerial.print(" PREMAX="); CmdSerial.print(cfg.prechargeMaxBursts);
  CmdSerial.print(" Vsec="); CmdSerial.print(vAfter, 3);
  CmdSerial.println(" V");
}

void finishAutotuneStopped() {
  autoTuneRunning = false;
  flushPendingSettingsSave(false);
}

void autoTunePrecharge() {
  if (autoTuneRunning) return;
  autoTuneRunning = true;

  CmdSerial.println();
  CmdSerial.println("================================================");
  CmdSerial.println("AUTOPRE START: tuning initial secondary-feedback burst");
  CmdSerial.println("================================================");

  systemEnabled = true;
  controlMode = MODE_OPEN_LOOP;
  faultLatched = false;
  faultCode = FAULT_NONE;
  startupPhase = STARTUP_IDLE;
  startupBurstCount = 0;
  filtersPrimed = false;
  setGateOutputsEnabled(true);
  setEnFrequencyHz(cfg.enFreqHz);
  setEnDutyX10(0);

  for (uint8_t i = 0; i < 5; i++) {
    updateAnalogFilters(true);
    delay(2);
  }

  if (cfg.prechargeReadyV <= 0.0f || (filteredVsec >= cfg.prechargeReadyV && filteredVsec <= cfg.secMaxV)) {
    savePrechargeTuneResult(cfg.prechargeDutyX10, cfg.prechargeMaxBursts, filteredVsec);
    CmdSerial.println("Secondary feedback already above PREV; existing precharge kept.");
    finishAutotuneStopped();
    CmdSerial.print("> ");
    return;
  }

  uint16_t startDuty = cfg.prechargeDutyX10;
  if (startDuty < 1) startDuty = 1;
  uint16_t maxDuty = cfg.prechargeTuneMaxDutyX10;
  if (maxDuty < startDuty) maxDuty = startDuty;

  bool found = false;
  uint16_t foundDuty = startDuty;
  uint8_t foundBursts = 1;
  float foundV = filteredVsec;

  for (uint16_t d = startDuty; d <= maxDuty; d++) {
    for (uint8_t burst = 1; burst <= cfg.prechargeTuneMaxBursts; burst++) {
      float vAfter = 0.0f;
      float iMax = 0.0f;
      bool highStop = false;
      bool ok = runPrechargeTuneBurst(d, cfg.prechargeBurstMs, vAfter, iMax, highStop);

      CmdSerial.print("PRETRY D="); CmdSerial.print(dutyX10ToPercent(d), 2);
      CmdSerial.print("% burst "); CmdSerial.print(burst);
      CmdSerial.print(" Vsec="); CmdSerial.print(vAfter, 3);
      CmdSerial.print("V Imax="); CmdSerial.print(iMax, 3);
      CmdSerial.println(highStop ? "A HIGHV_STOP" : "A");

      if (!ok) {
        CmdSerial.println("AUTOPRE FAILED: fault during precharge tune.");
        setEnDutyX10(0);
        systemEnabled = false;
        cfg.systemEnabled = 0;
        finishAutotuneStopped();
        CmdSerial.print("> ");
        return;
      }

      if (highStop) {
        CmdSerial.println("AUTOPRE STOPPED: secondary voltage exceeded VMAX before a safe result was saved.");
        setEnDutyX10(0);
        systemEnabled = false;
        cfg.systemEnabled = 0;
        saveSettings();
        finishAutotuneStopped();
        CmdSerial.print("> ");
        return;
      }

      if (cfg.prechargeReadyV <= 0.0f || vAfter >= cfg.prechargeReadyV) {
        found = true;
        foundDuty = d;
        foundBursts = burst;
        foundV = vAfter;
        break;
      }
    }

    if (found) break;
    if (d == maxDuty) break;
  }

  if (found) {
    savePrechargeTuneResult(foundDuty, foundBursts, foundV);
  } else {
    CmdSerial.println("AUTOPRE did not reach PREV within PREAUTOMAX/PRETRIES. Settings not changed.");
    setEnDutyX10(0);
    systemEnabled = false;
    cfg.systemEnabled = 0;
    saveSettings();
  }

  finishAutotuneStopped();
  CmdSerial.print("> ");
}

void setSystemEnabled(bool enable, bool save) {
  systemEnabled = enable;
  cfg.systemEnabled = enable ? 1 : 0;
  if (!enable) {
    startupPhase = STARTUP_IDLE;
    startupPhaseStartMs = 0;
    startupBurstCount = 0;
    setEnDutyX10(0);
    powerIntegratorPct = 0.0f;
    bangBangHigh = false;
    bangBangLastSwitchMs = millis();
    maxDutyStartMs = 0;
  } else {
    setGateOutputsEnabled(true);
    setEnFrequencyHz(cfg.enFreqHz);
    filtersPrimed = false;
    beginStartupPrecharge();
  }
  updateModeLEDs();
  if (save) saveSettings();
}

void setMode(ControlMode mode, bool save) {
  controlMode = mode;
  cfg.controlMode = (uint8_t)mode;
  powerIntegratorPct = 0.0f;
  bangBangHigh = false;
  bangBangLastSwitchMs = millis();
  controlDutyPercent = dutyX10ToPercent(cfg.bangLowDutyX10);
  if (systemEnabled) {
    if (!startupPrechargeActive()) {
      if (mode == MODE_OPEN_LOOP) setEnDutyX10(cfg.openLoopDutyX10);
      else setEnDutyX10(cfg.bangLowDutyX10);
    }
  }
  updateModeLEDs();
  if (save) saveSettings();
}

// ============================================================
// Bang-bang control
// ============================================================

float highVoltageFoldbackPct() {
  if (filteredVsec <= cfg.secMaxV) return 0.0f;
  return -cfg.secHighFoldPctPerV * (filteredVsec - cfg.secMaxV);
}

float lowVoltageBoostPct() {
  if (filteredVsec >= cfg.secMinV) return 0.0f;
  return cfg.secLowBoostPctPerV * (cfg.secMinV - filteredVsec);
}

float currentFoldbackPct() {
  if (!cfg.currentFoldbackEnable) return 0.0f;
  if (filteredCurrent <= cfg.currentSoftA) return 0.0f;
  return -cfg.currentFoldPctPerA * (filteredCurrent - cfg.currentSoftA);
}

void handleMaxDutyProtection(float errW) {
  if (!cfg.maxDutyFaultEnable || cfg.dutyMaxX10 < 1) {
    maxDutyStartMs = 0;
    return;
  }
  if (enDutyEffX10 >= cfg.dutyMaxX10 - 2 && errW > ((float)cfg.maxDutyFaultErrMw / 1000.0f)) {
    if (maxDutyStartMs == 0) maxDutyStartMs = millis();
    if (millis() - maxDutyStartMs >= cfg.maxDutyFaultMs) {
      latchFault(FAULT_MAX_DUTY, "max duty without reaching power target");
    }
  } else {
    maxDutyStartMs = 0;
  }
}

void handlePowerLoop() {
  static uint32_t lastControlUs = 0;

  if (!systemEnabled || controlMode != MODE_POWER_LOOP) return;
  if (faultLatched) {
    setEnDutyX10(0);
    return;
  }

  uint32_t nowUs = micros();
  if (lastControlUs == 0) {
    lastControlUs = nowUs;
    return;
  }
  uint32_t elapsedUs = nowUs - lastControlUs;
  if (elapsedUs < cfg.controlPeriodUs) return;

  if (elapsedUs > cfg.controlPeriodUs + (cfg.controlPeriodUs / 2UL)) controlOverrunCount++;
  lastControlUs = nowUs;
  lastControlDtUs = elapsedUs;
  if (elapsedUs > maxControlDtUs) maxControlDtUs = elapsedUs;

  float dt = ((float)elapsedUs) / 1000000.0f;
  dt = clampFloat(dt, 0.00002f, 0.1f);

  updateAnalogFilters(true);
  if (checkFaults()) return;

  (void)dt;
  float errW = cfg.targetPowerW - filteredPower;
  float hystW = ((float)cfg.bangHystMw) / 1000.0f;
  if (hystW <= 0.0f) hystW = ((float)cfg.deadbandMw) / 1000.0f;
  if (hystW < 0.0f) hystW = 0.0f;

  float lowThreshold = cfg.targetPowerW - hystW;
  float highThreshold = cfg.targetPowerW + hystW;
  uint32_t nowMs = millis();
  uint32_t dwellMs = nowMs - bangBangLastSwitchMs;

  bool forceLow = false;
  if (filteredVsec >= cfg.secMaxV) forceLow = true;
  if (cfg.currentFoldbackEnable && filteredCurrent >= cfg.currentSoftA) forceLow = true;

  if (forceLow && bangBangHigh) {
    bangBangHigh = false;
    bangBangLastSwitchMs = nowMs;
  } else if (bangBangHigh) {
    if (filteredPower >= highThreshold && dwellMs >= cfg.bangMinOnMs) {
      bangBangHigh = false;
      bangBangLastSwitchMs = nowMs;
    }
  } else {
    if (!forceLow && filteredPower <= lowThreshold && dwellMs >= cfg.bangMinOffMs) {
      bangBangHigh = true;
      bangBangLastSwitchMs = nowMs;
    }
  }

  uint16_t desiredDuty = bangBangHigh ? cfg.bangHighDutyX10 : cfg.bangLowDutyX10;
  if (desiredDuty < cfg.dutyMinX10) desiredDuty = cfg.dutyMinX10;
  if (desiredDuty > cfg.dutyMaxX10) desiredDuty = cfg.dutyMaxX10;
  controlDutyPercent = dutyX10ToPercent(desiredDuty);
  setEnDutyX10(desiredDuty);
  handleMaxDutyProtection(errW);
}

// ============================================================
// Autotune
// ============================================================

void initMeasure(MeasureResult &m) {
  memset(&m, 0, sizeof(m));
  m.minVsec = 99999.0f;
  m.maxVsec = -99999.0f;
  m.minP = 99999.0f;
  m.maxP = -99999.0f;
}

bool serviceDelayMs(uint32_t ms) {
  uint32_t start = millis();
  while (millis() - start < ms) {
    handlePowerLoop();
    updateAnalogFilters(true);
    if (checkFaults()) return false;
    if (autoTuneRunning && filteredVsec > cfg.secMaxV) {
      setEnDutyX10(0);
      return false;
    }
    delay(1);
  }
  return true;
}

MeasureResult measureWindow(uint32_t ms) {
  MeasureResult m;
  initMeasure(m);
  uint32_t sumBlock = 0;
  uint32_t start = millis();

  while (millis() - start < ms) {
    updateAnalogFilters(true);
    if (checkFaults()) {
      m.fault = true;
      break;
    }

    float p = latestPowerRaw;
    m.avgVpri += latestVpriRaw;
    m.avgVsec += latestVsecRaw;
    m.avgI += latestCurrentRaw;
    m.avgP += p;
    if (latestVsecRaw < m.minVsec) m.minVsec = latestVsecRaw;
    if (latestVsecRaw > m.maxVsec) m.maxVsec = latestVsecRaw;
    if (p < m.minP) m.minP = p;
    if (p > m.maxP) m.maxP = p;
    sumBlock += lastAdcBlockUs;
    m.count++;

    if (latestVsecRaw > cfg.secMaxV) {
      m.highVStop = true;
      setEnDutyX10(0);
      break;
    }

    delay(2);
  }

  if (m.count == 0) m.count = 1;
  m.avgVpri /= (float)m.count;
  m.avgVsec /= (float)m.count;
  m.avgI /= (float)m.count;
  m.avgP /= (float)m.count;
  m.avgBlockUs = sumBlock / m.count;
  m.valid = feedbackMeasurementValid(m.avgVpri, m.avgVsec, m.avgI, m.avgP);
  return m;
}

MeasureResult settleAndMeasure(uint32_t settleMs, uint32_t measureMs) {
  if (!serviceDelayMs(settleMs)) {
    MeasureResult m;
    initMeasure(m);
    updateAnalogFilters(true);
    m.avgVpri = filteredVpri;
    m.avgVsec = filteredVsec;
    m.minVsec = filteredVsec;
    m.maxVsec = filteredVsec;
    m.avgI = filteredCurrent;
    m.avgP = filteredPower;
    m.minP = filteredPower;
    m.maxP = filteredPower;
    m.count = 1;
    m.avgBlockUs = lastAdcBlockUs;
    m.valid = feedbackMeasurementValid(filteredVpri, filteredVsec, filteredCurrent, filteredPower);
    m.fault = faultLatched;
    m.highVStop = filteredVsec > cfg.secMaxV;
    return m;
  }
  return measureWindow(measureMs);
}

void printMeasure(const char *tag, uint32_t freqHz, uint16_t dutyX10, const MeasureResult &m, float score) {
  CmdSerial.print(tag);
  CmdSerial.print(" FEN="); CmdSerial.print(freqHz);
  CmdSerial.print("Hz D="); CmdSerial.print(dutyX10ToPercent(dutyX10), 1);
  CmdSerial.print("% Pfb="); CmdSerial.print(m.avgP, 3);
  CmdSerial.print("W Vpri="); CmdSerial.print(m.avgVpri, 2);
  CmdSerial.print("V I="); CmdSerial.print(m.avgI, 3);
  CmdSerial.print("A Vsec="); CmdSerial.print(m.avgVsec, 3);
  CmdSerial.print(" min/max="); CmdSerial.print(m.minVsec, 3);
  CmdSerial.print("/"); CmdSerial.print(m.maxVsec, 3);
  CmdSerial.print(" score="); CmdSerial.print(score, 3);
  if (!m.valid) CmdSerial.print(" INVALID");
  if (m.fault) CmdSerial.print(" FAULT");
  if (m.highVStop) CmdSerial.print(" HIGHV_STOP");
  CmdSerial.println();
}

float scorePowerPoint(uint32_t freqHz, uint16_t dutyX10, const MeasureResult &m, int8_t loadSlot) {
  if (!m.valid || m.fault) return 999999.0f;

  float score = fabsf(cfg.targetPowerW - m.avgP);
  float rippleP = m.maxP - m.minP;
  if (isfinite(rippleP) && rippleP > 0.0f) score += 0.05f * rippleP;

  if (m.avgVsec < cfg.secMinV) score += (cfg.secMinV - m.avgVsec) * 10.0f;
  if (m.avgVsec > cfg.secMaxV) score += (m.avgVsec - cfg.secMaxV) * 20.0f;
  if (m.maxVsec > cfg.secOvpV) score += 1000.0f;

  float freqPref = (float)cfg.enFreqPrefHz;
  if (freqPref > 0.0f && cfg.enFreqPenaltyW > 0.0f) {
    score += (fabsf((float)freqHz - freqPref) / freqPref) * cfg.enFreqPenaltyW;
  }

  score += dutyX10ToPercent(dutyX10) * 0.005f;

  if (cfg.powerFeedbackMode == PFB_SECONDARY_VI && loadSlot >= 0 && validLoadSlot((uint8_t)loadSlot)) {
    float r = calLoadOhms((uint8_t)loadSlot);
    if (r > 0.0f && m.avgVsec > 1.0f && m.avgI > 0.001f) {
      float expectedSecondaryP = (m.avgVsec * m.avgVsec) / r;
      float mismatch = fabsf(expectedSecondaryP - m.avgP);
      score += 0.01f * mismatch;
    }
  }

  return score;
}

bool considerTunePoint(const char *tag, uint32_t freqHz, uint16_t dutyX10, int8_t loadSlot,
                       uint32_t &bestFreq, uint16_t &bestDuty,
                       float &bestScore, MeasureResult &bestMeasure) {
  setEnFrequencyHz(freqHz);
  setEnDutyX10(dutyX10);
  filtersPrimed = false;
  MeasureResult m = settleAndMeasure(cfg.autotuneSettleMs, cfg.autotuneMeasureMs);
  lastTunePointHighVStop = m.highVStop || m.maxVsec > cfg.secMaxV;
  float score = scorePowerPoint(freqHz, dutyX10, m, loadSlot);
  printMeasure(tag, freqHz, dutyX10, m, score);
  if (m.fault) return false;
  if (m.valid && score < bestScore) {
    bestScore = score;
    bestFreq = freqHz;
    bestDuty = dutyX10;
    bestMeasure = m;
  }
  return true;
}

bool autotunePowerFull(int8_t loadSlot, uint32_t &bestFreq, uint16_t &bestDuty, MeasureResult &bestMeasure) {
  CmdSerial.println();
  CmdSerial.println("AUTOBANG: fixed-frequency EN duty calibration");
  CmdSerial.print("FEN fixed at "); CmdSerial.print(cfg.enFreqHz); CmdSerial.println(" Hz");

  uint16_t loDuty = cfg.dutyMinX10;
  if (cfg.bangLowDutyX10 > loDuty) loDuty = cfg.bangLowDutyX10;
  uint16_t hiDuty = cfg.autotuneMaxDutyX10;
  if (hiDuty > cfg.dutyMaxX10) hiDuty = cfg.dutyMaxX10;
  if (hiDuty < loDuty + cfg.autotuneCoarseStepX10) hiDuty = loDuty + cfg.autotuneCoarseStepX10;
  if (hiDuty > cfg.dutyMaxX10) hiDuty = cfg.dutyMaxX10;

  bestFreq = cfg.enFreqHz;
  bestDuty = cfg.bangHighDutyX10;
  float bestScore = 999999.0f;
  initMeasure(bestMeasure);

  bool ok = true;

  setEnFrequencyHz(cfg.enFreqHz);
  for (uint16_t d = loDuty; d <= hiDuty; ) {
    ok = considerTunePoint("BANG", cfg.enFreqHz, d, loadSlot, bestFreq, bestDuty, bestScore, bestMeasure);
    if (!ok) return false;
    if (lastTunePointHighVStop) break;
    if (hiDuty - d < cfg.autotuneCoarseStepX10) break;
    d = (uint16_t)(d + cfg.autotuneCoarseStepX10);
  }

  // Fine duty scan around the best point.
  uint16_t fine = cfg.autotuneFineStepX10;
  if (fine < 1) fine = 1;
  int32_t start = (int32_t)bestDuty - (int32_t)cfg.autotuneCoarseStepX10;
  int32_t stop = (int32_t)bestDuty + (int32_t)cfg.autotuneCoarseStepX10;
  if (start < (int32_t)loDuty) start = loDuty;
  if (stop > (int32_t)hiDuty) stop = hiDuty;
  for (uint16_t d = (uint16_t)start; d <= (uint16_t)stop; ) {
    ok = considerTunePoint("BFINE", cfg.enFreqHz, d, loadSlot, bestFreq, bestDuty, bestScore, bestMeasure);
    if (!ok) return false;
    if (lastTunePointHighVStop) break;
    if ((uint16_t)stop - d < fine) break;
    d = (uint16_t)(d + fine);
  }

  if (bestScore >= 999000.0f) return false;
  setEnFrequencyHz(bestFreq);
  setEnDutyX10(bestDuty);
  return true;
}

bool autotuneIdentifyPlant(uint16_t baseDutyX10, float &gainWPerPct, float &tauS) {
  CmdSerial.println("AUTOPOWER: plant gain/tau estimate");
  gainWPerPct = 0.0f;
  tauS = 0.20f;

  setEnDutyX10(baseDutyX10);
  filtersPrimed = false;
  MeasureResult base = settleAndMeasure(300, 160);
  float baseP = base.avgP;
  if (!base.valid || base.fault) return false;

  int16_t step = cfg.autotuneTestStepX10;
  if ((int32_t)baseDutyX10 + step > cfg.dutyMaxX10) step = -step;
  if ((int32_t)baseDutyX10 + step < cfg.dutyMinX10) step = cfg.autotuneTestStepX10;

  uint16_t stepDuty = clampDutyX10((int32_t)baseDutyX10 + step);
  if (stepDuty > cfg.dutyMaxX10) stepDuty = cfg.dutyMaxX10;
  if (stepDuty < cfg.dutyMinX10) stepDuty = cfg.dutyMinX10;
  float actualStepPct = ((float)((int32_t)stepDuty - (int32_t)baseDutyX10)) / 10.0f;
  if (fabsf(actualStepPct) < 0.2f) return false;

  const uint8_t MAX_SAMPLES = 80;
  float p[MAX_SAMPLES];
  float t[MAX_SAMPLES];
  uint8_t n = 0;

  setEnDutyX10(stepDuty);
  uint32_t startMs = millis();
  while (millis() - startMs < 600UL && n < MAX_SAMPLES) {
    updateAnalogFilters(true);
    if (checkFaults()) return false;
    p[n] = latestPowerRaw;
    t[n] = ((float)(millis() - startMs)) / 1000.0f;
    n++;
    delay(5);
  }
  setEnDutyX10(baseDutyX10);

  if (n < 8) return false;
  float finalP = 0.0f;
  uint8_t count = 0;
  for (uint8_t i = (uint8_t)((n * 2) / 3); i < n; i++) {
    finalP += p[i];
    count++;
  }
  if (count == 0) count = 1;
  finalP /= (float)count;

  float deltaP = finalP - baseP;
  gainWPerPct = fabsf(deltaP / actualStepPct);
  if (gainWPerPct < 0.02f) {
    if (baseDutyX10 > 10 && baseP > 0.5f) gainWPerPct = baseP / dutyX10ToPercent(baseDutyX10);
  }
  if (gainWPerPct < 0.02f) gainWPerPct = 0.20f;

  float threshold = baseP + 0.632f * deltaP;
  bool found = false;
  for (uint8_t i = 0; i < n; i++) {
    if (actualStepPct > 0.0f) {
      if (p[i] >= threshold) { tauS = t[i]; found = true; break; }
    } else {
      if (p[i] <= threshold) { tauS = t[i]; found = true; break; }
    }
  }
  if (!found) tauS = 0.20f;
  tauS = clampFloat(tauS, 0.020f, 2.000f);

  CmdSerial.print("Power gain=");
  CmdSerial.print(gainWPerPct, 5);
  CmdSerial.print(" W/%, tau=");
  CmdSerial.print(tauS, 3);
  CmdSerial.println(" s");
  return true;
}

void autotuneComputePI(float gainWPerPct, float tauS) {
  float lambda = 4.0f * tauS;
  lambda = clampFloat(lambda, 0.050f, 1.500f);

  float kp = tauS / (gainWPerPct * lambda);
  float ki = kp / tauS;
  kp *= 0.55f;
  ki *= 0.35f;

  kp = clampFloat(kp, 0.005f, 50.0f);
  ki = clampFloat(ki, 0.00f, 200.0f);
  cfg.kp_x1000 = (int32_t)(kp * 1000.0f + 0.5f);
  cfg.ki_x1000 = (int32_t)(ki * 1000.0f + 0.5f);
}

void storeLoadProfile(uint8_t slot, uint32_t freqHz, uint16_t dutyX10,
                      float gain, float tau, const MeasureResult &m) {
  if (!validLoadSlot(slot)) return;
  cfg.activeCalLoadSlot = slot;
  cfg.calLoadFreqHz[slot] = freqHz;
  cfg.calLoadDutyX10[slot] = dutyX10;
  cfg.calLoadKp_x1000[slot] = cfg.kp_x1000;
  cfg.calLoadKi_x1000[slot] = cfg.ki_x1000;
  cfg.calLoadGainWPerPct[slot] = gain;
  cfg.calLoadTauS[slot] = tau;
  cfg.calLoadTargetW[slot] = cfg.targetPowerW;
  cfg.calLoadMeasuredW[slot] = m.avgP;
  cfg.calLoadMeasuredVsec[slot] = m.avgVsec;
  cfg.calLoadMeasuredI[slot] = m.avgI;
}

void applyLoadProfile(uint8_t slot, bool save) {
  if (!validLoadSlot(slot)) return;
  cfg.activeCalLoadSlot = slot;
  if (loadProfileValid(slot)) {
    cfg.enFreqHz = cfg.calLoadFreqHz[slot];
    cfg.biasDutyX10 = cfg.calLoadDutyX10[slot];
    cfg.bangHighDutyX10 = cfg.calLoadDutyX10[slot];
    cfg.kp_x1000 = cfg.calLoadKp_x1000[slot];
    cfg.ki_x1000 = cfg.calLoadKi_x1000[slot];
    cfg.tunedPlantGainWPerPct = cfg.calLoadGainWPerPct[slot];
    cfg.tunedPlantTauS = cfg.calLoadTauS[slot];
    cfg.tunedDutyX10 = cfg.calLoadDutyX10[slot];
    cfg.tunedTargetW = cfg.calLoadTargetW[slot];
    setEnFrequencyHz(cfg.enFreqHz);
  }
  if (save) saveSettings();
}

void autoTunePower(bool fullScan, int8_t loadSlot) {
  (void)fullScan; // This fresh power version always uses the full grid.
  if (autoTuneRunning) return;
  autoTuneRunning = true;

  CmdSerial.println();
  CmdSerial.println("================================================");
  CmdSerial.println("AUTOBANG START: fixed-frequency PA10 EN duty calibration");
  CmdSerial.println("================================================");

  systemEnabled = true;
  controlMode = MODE_OPEN_LOOP;
  faultLatched = false;
  faultCode = FAULT_NONE;
  filtersPrimed = false;
  maxDutyStartMs = 0;
  setGateOutputsEnabled(true);
  setEnFrequencyHz(cfg.enFreqHz);
  updateModeLEDs();

  if (!runStartupPrechargeBlocking()) {
    setEnDutyX10(0);
    autoTuneRunning = false;
    CmdSerial.println("AUTOBANG FAILED: startup precharge fault.");
    CmdSerial.print("> ");
    return;
  }

  if (loadSlot >= 0 && validLoadSlot((uint8_t)loadSlot)) {
    cfg.activeCalLoadSlot = (uint8_t)loadSlot;
    CmdSerial.print("Load slot ");
    CmdSerial.print((int)loadSlot + 1);
    CmdSerial.print(" R=");
    CmdSerial.print(calLoadOhms((uint8_t)loadSlot), 3);
    CmdSerial.println(" ohm");
  }

  uint32_t bestFreq = cfg.enFreqHz;
  uint16_t bestDuty = cfg.biasDutyX10;
  MeasureResult bestMeasure;
  initMeasure(bestMeasure);
  if (!autotunePowerFull(loadSlot, bestFreq, bestDuty, bestMeasure)) {
    setEnDutyX10(0);
    autoTuneRunning = false;
    CmdSerial.println("AUTOBANG FAILED: no safe duty point found.");
    CmdSerial.print("> ");
    return;
  }

  cfg.enFreqHz = bestFreq;
  cfg.bangHighDutyX10 = bestDuty;
  cfg.biasDutyX10 = bestDuty;
  if (cfg.bangLowDutyX10 < cfg.dutyMinX10) cfg.bangLowDutyX10 = cfg.dutyMinX10;
  if (cfg.bangLowDutyX10 >= cfg.bangHighDutyX10) cfg.bangLowDutyX10 = cfg.dutyMinX10;
  cfg.tunedDutyX10 = bestDuty;
  cfg.tunedTargetW = cfg.targetPowerW;
  cfg.tunedPlantGainWPerPct = 0.0f;
  cfg.tunedPlantTauS = 0.0f;
  if (loadSlot >= 0 && validLoadSlot((uint8_t)loadSlot)) {
    storeLoadProfile((uint8_t)loadSlot, bestFreq, bestDuty, 0.0f, 0.0f, bestMeasure);
  }

  controlMode = MODE_POWER_LOOP;
  cfg.controlMode = MODE_POWER_LOOP;
  powerIntegratorPct = 0.0f;
  bangBangHigh = false;
  bangBangLastSwitchMs = millis();
  controlDutyPercent = dutyX10ToPercent(cfg.bangLowDutyX10);
  setEnFrequencyHz(bestFreq);
  setEnDutyX10(cfg.bangLowDutyX10);
  updateModeLEDs();
  saveSettings();

  CmdSerial.println();
  CmdSerial.println("AUTOBANG RESULT");
  CmdSerial.print("FEN="); CmdSerial.print(bestFreq); CmdSerial.println(" Hz");
  CmdSerial.print("BLOW="); CmdSerial.print(dutyX10ToPercent(cfg.bangLowDutyX10), 2); CmdSerial.print(" %, ");
  CmdSerial.print("BHIGH="); CmdSerial.print(dutyX10ToPercent(bestDuty), 2); CmdSerial.println(" %");
  CmdSerial.print("BHYST="); CmdSerial.print(((float)cfg.bangHystMw) / 1000.0f, 3); CmdSerial.println(" W");
  CmdSerial.print("Feedback source="); CmdSerial.println(powerFeedbackName());
  CmdSerial.print("Measured Pfb="); CmdSerial.print(bestMeasure.avgP, 3); CmdSerial.print(" W, target=");
  CmdSerial.print(cfg.targetPowerW, 3); CmdSerial.println(" W");
  CmdSerial.print("Measured Vsec="); CmdSerial.print(bestMeasure.avgVsec, 3); CmdSerial.print(" V, I=");
  CmdSerial.print(bestMeasure.avgI, 3); CmdSerial.println(" A");
  if (settingsDirty) CmdSerial.println("AUTOBANG COMPLETE. Applied in RAM; EEPROM save pending until OFF.");
  else CmdSerial.println("AUTOBANG COMPLETE. Settings saved.");
  CmdSerial.print("> ");
  autoTuneRunning = false;
}

// ============================================================
// UART
// ============================================================

const char *modeName() {
  return controlMode == MODE_OPEN_LOOP ? "OPEN" : "BANG";
}

void printLiveStatusLine() {
  CmdSerial.print("\rPfb="); CmdSerial.print(filteredPower, 2); CmdSerial.print("W");
  CmdSerial.print(" Vpri="); CmdSerial.print(filteredVpri, 1);
  CmdSerial.print("V I="); CmdSerial.print(filteredCurrent, 3);
  CmdSerial.print("A Vsec="); CmdSerial.print(filteredVsec, 2);
  CmdSerial.print("V D="); CmdSerial.print(getEffDutyPercent(), 1);
  CmdSerial.print("% FEN="); CmdSerial.print(enFreqRuntimeHz);
  CmdSerial.print("Hz mode="); CmdSerial.print(modeName());
  if (controlMode == MODE_POWER_LOOP) { CmdSerial.print(" B="); CmdSerial.print(bangBangHigh ? "H" : "L"); }
  if (startupPrechargeActive()) { CmdSerial.print(" startup="); CmdSerial.print(startupPhaseName()); }
  if (filteredVsec < cfg.secMinV) CmdSerial.print(" VLOW");
  if (filteredVsec > cfg.secMaxV) CmdSerial.print(" VHIGH");
  if (faultLatched) { CmdSerial.print(" FAULT="); CmdSerial.print(faultName()); }
  CmdSerial.print("                              ");
}

void printParams() {
  CmdSerial.println();
  CmdSerial.println("SET-able parameters:");
  CmdSerial.println("PFBSRC");
  CmdSerial.println("PTARGET, VREF, VPRITOP, VPRIBOT, VPRIGAIN, VPRIOFF");
  CmdSerial.println("AMCREF, AMCVCLIP, VSECTOP, VSECBOT, VSECGAIN, VSECOFF");
  CmdSerial.println("CSRES, CSGAIN, CSOFF, IABS, ITRIP, ITRIPEN, ISOFT, IFOLDEN, IFOLD");
  CmdSerial.println("PRECHEN, PREDUTY, PREMS, PRESETTLE, PREMAX, PREV, PREAUTOMAX, PRETRIES");
  CmdSerial.println("FEN, FMIN, FMAX, FPREF, FPEN, MINEDGE, GATECYC, GATELEAD, STATIC, DMIN, DMAX, OD, BIAS, PWRDUTY");
  CmdSerial.println("BLOW, BHIGH, BHYST, BONMS, BOFFMS");
  CmdSerial.println("CPER, STATUSMS, PTAU, VPTAU, VSTAU, ITAU");
  CmdSerial.println("KP, KI, DB, SLEW, IMIN, IMAX");
  CmdSerial.println("VMIN, VMAX, OVP, OVPEN, VBOOST, VFOLD, MAXFAULTEN, MAXFAULTMS, MAXFAULTERR");
  CmdSerial.println("AUTOMAX, AUTOSTEP, AUTOFINE, AUTOSETTLE, AUTOMEAS");
  CmdSerial.println("LOAD1, LOAD2, LOAD3");
  CmdSerial.println("Commands: ON, OFF, OPEN, BANG/POWER, PFBPRI, PFBSEC, AUTOPRE, AUTOBANG/CAL, CALLOAD n, CAL3, LOAD n, ZEROI, FAST, TURBO, CLR, SAVE, DEFAULTS");
}

void printDividerAdvice() {
  CmdSerial.println();
  CmdSerial.println("PA0 primary divider options to 3.3 V ADC:");
  CmdSerial.println("  Selected for 450 V peak: Rtop 1.50M, Rbot 10k -> PA0 about 2.98 V");
  CmdSerial.println("  Higher ADC use at 450 V: Rtop 1.43M, Rbot 10k -> PA0 about 3.13 V");
  CmdSerial.println("  Do not use 1.24M/10k at 450 V; PA0 would be about 3.60 V.");
  CmdSerial.println("  Up to 600 V: Rtop 1.82M, Rbot 10k -> PA0 about 3.28 V at 600 V");
  CmdSerial.println("Use series parts for Rtop, e.g. 3x499k for 1.50M, and set VPRITOP/VPRIBOT to actual kOhms.");
}

void printStatus() {
  updateAnalogFilters(true);

  CmdSerial.println();
  CmdSerial.println("========== BANG-BANG CONTROL STATUS ==========");
  CmdSerial.print("Firmware: "); CmdSerial.print(FW_VERSION_STRING);
  CmdSerial.print(" EEPROM magic "); CmdSerial.println(EEPROM_MAGIC_NAME);
  CmdSerial.print("System: "); CmdSerial.println(systemEnabled ? "ON" : "OFF");
  CmdSerial.print("Mode: "); CmdSerial.println(modeName());
  CmdSerial.print("Startup state: "); CmdSerial.print(startupPhaseName());
  CmdSerial.print(" bursts "); CmdSerial.print(startupBurstCount);
  CmdSerial.print("/"); CmdSerial.println(cfg.prechargeMaxBursts);
  CmdSerial.print("Fault: "); CmdSerial.println(faultLatched ? faultName() : "NONE");
  CmdSerial.print("Target power: "); CmdSerial.print(cfg.targetPowerW, 3); CmdSerial.println(" W");
  CmdSerial.print("Power feedback source: "); CmdSerial.println(powerFeedbackName());

  CmdSerial.print("Measured Pfb/Vpri/I/Vsec: ");
  CmdSerial.print(filteredPower, 3); CmdSerial.print(" W / ");
  CmdSerial.print(filteredVpri, 3); CmdSerial.print(" V / ");
  CmdSerial.print(filteredCurrent, 4); CmdSerial.print(" A / ");
  CmdSerial.print(filteredVsec, 3); CmdSerial.println(" V");
  CmdSerial.print("Raw PA0/PA1/PA2 ADC,V: ");
  CmdSerial.print(rawPa0Adc); CmdSerial.print(","); CmdSerial.print(rawPa0Voltage, 5); CmdSerial.print(" / ");
  CmdSerial.print(rawPa1Adc); CmdSerial.print(","); CmdSerial.print(rawPa1Voltage, 5); CmdSerial.print(" / ");
  CmdSerial.print(rawPa2Adc); CmdSerial.print(","); CmdSerial.print(rawPa2Voltage, 5); CmdSerial.println();
  CmdSerial.print("ADC DMA running/errors/latest: ");
  CmdSerial.print(adcDmaRunning ? "YES" : "NO"); CmdSerial.print(" / ");
  CmdSerial.print(adcDmaStartErrors); CmdSerial.print(" / ");
  CmdSerial.print(adcDmaBuffer[ADC_DMA_VPRI_INDEX]); CmdSerial.print(",");
  CmdSerial.print(adcDmaBuffer[ADC_DMA_VSEC_INDEX]); CmdSerial.print(",");
  CmdSerial.println(adcDmaBuffer[ADC_DMA_I_INDEX]);

  CmdSerial.print("PA10 EN freq/min/max/pref: ");
  CmdSerial.print(enFreqRuntimeHz); CmdSerial.print(" / "); CmdSerial.print(cfg.enFreqMinHz);
  CmdSerial.print(" / "); CmdSerial.print(cfg.enFreqMaxHz); CmdSerial.print(" / "); CmdSerial.println(cfg.enFreqPrefHz);
  CmdSerial.print("PA10 duty cmd/effective/min/max: ");
  CmdSerial.print(getCmdDutyPercent(), 2); CmdSerial.print(" / "); CmdSerial.print(getEffDutyPercent(), 2);
  CmdSerial.print(" / "); CmdSerial.print(dutyX10ToPercent(cfg.dutyMinX10), 1);
  CmdSerial.print(" / "); CmdSerial.print(dutyX10ToPercent(cfg.dutyMaxX10), 1); CmdSerial.println(" %");
  CmdSerial.print("PA10 period/drive-us/drive-cyc/minedge/gatecyc/gatelead/gatemin/static100: ");
  CmdSerial.print(enPeriodUs); CmdSerial.print("/"); CmdSerial.print(enHighUs); CmdSerial.print("/");
  CmdSerial.print(enHighGateCycles); CmdSerial.print("/");
  CmdSerial.print(cfg.enMinEdgeUs); CmdSerial.print("/");
  CmdSerial.print(cfg.enMinGateCycles); CmdSerial.print("/");
  CmdSerial.print(cfg.enGateLeadCycles); CmdSerial.print("/");
  CmdSerial.print(minCompleteGateBurstUs()); CmdSerial.print(" us / "); CmdSerial.println(cfg.allowStatic100 ? "YES" : "NO");
  CmdSerial.print("PA10 carrier-sync rise/drive/fall/abort/carrier: ");
  CmdSerial.print(enSyncRiseCount); CmdSerial.print("/");
  CmdSerial.print(enSyncDriveStartCount); CmdSerial.print("/");
  CmdSerial.print(enSyncFallCount); CmdSerial.print("/");
  CmdSerial.print(enSyncAbortCount); CmdSerial.print("/");
  CmdSerial.println(enSyncCarrierActive ? "ON" : "OFF");
  CmdSerial.print("PA10 low-duty pulse skip: every ");
  CmdSerial.print(enPulseSkipN);
  CmdSerial.print(" periods, avg duty ");
  CmdSerial.print(getEffDutyPercent(), 2);
  CmdSerial.print(" %, limit bypass ");
  CmdSerial.println(enDutyLimitBypass ? "YES" : "NO");
  CmdSerial.print("Startup precharge en/duty/burst/settle/max/ready: ");
  CmdSerial.print(cfg.prechargeEnable ? "YES" : "NO"); CmdSerial.print(" / ");
  CmdSerial.print(dutyX10ToPercent(cfg.prechargeDutyX10), 2); CmdSerial.print(" % / ");
  CmdSerial.print(cfg.prechargeBurstMs); CmdSerial.print(" ms / ");
  CmdSerial.print(cfg.prechargeSettleMs); CmdSerial.print(" ms / ");
  CmdSerial.print(cfg.prechargeMaxBursts); CmdSerial.print(" / ");
  CmdSerial.print(cfg.prechargeReadyV, 2); CmdSerial.println(" V");
  CmdSerial.print("Startup precharge autotune max duty/tries: ");
  CmdSerial.print(dutyX10ToPercent(cfg.prechargeTuneMaxDutyX10), 2);
  CmdSerial.print(" % / "); CmdSerial.println(cfg.prechargeTuneMaxBursts);

  CmdSerial.print("Secondary guard min/max/OVP: ");
  CmdSerial.print(cfg.secMinV, 2); CmdSerial.print(" / "); CmdSerial.print(cfg.secMaxV, 2);
  CmdSerial.print(" / "); CmdSerial.print(cfg.secOvpV, 2); CmdSerial.println(" V");
  CmdSerial.print("Secondary guard boost/foldback: ");
  CmdSerial.print(cfg.secLowBoostPctPerV, 2); CmdSerial.print(" / ");
  CmdSerial.print(cfg.secHighFoldPctPerV, 2); CmdSerial.println(" % per V");
  CmdSerial.print("Bang low/high/hyst/state: ");
  CmdSerial.print(dutyX10ToPercent(cfg.bangLowDutyX10), 2); CmdSerial.print(" / ");
  CmdSerial.print(dutyX10ToPercent(cfg.bangHighDutyX10), 2); CmdSerial.print(" % / ");
  CmdSerial.print(((float)cfg.bangHystMw) / 1000.0f, 3); CmdSerial.print(" W / ");
  CmdSerial.println(bangBangHigh ? "HIGH" : "LOW");
  CmdSerial.print("Bang min on/off: ");
  CmdSerial.print(cfg.bangMinOnMs); CmdSerial.print(" / ");
  CmdSerial.print(cfg.bangMinOffMs); CmdSerial.println(" ms");

  CmdSerial.print("Control period range/requested/last/max/overruns: ");
  CmdSerial.print(CONTROL_PERIOD_MIN_US); CmdSerial.print("-");
  CmdSerial.print(CONTROL_PERIOD_MAX_US); CmdSerial.print(" / ");
  CmdSerial.print(cfg.controlPeriodUs); CmdSerial.print(" / "); CmdSerial.print(lastControlDtUs);
  CmdSerial.print(" / "); CmdSerial.print(maxControlDtUs); CmdSerial.print(" us / "); CmdSerial.println(controlOverrunCount);
  CmdSerial.print("ADC block last/max: "); CmdSerial.print(lastAdcBlockUs); CmdSerial.print(" / "); CmdSerial.print(maxAdcBlockUs); CmdSerial.println(" us");

  CmdSerial.print("PA0 divider top/bottom ratio: ");
  CmdSerial.print(cfg.vpriTopK, 2); CmdSerial.print("k / "); CmdSerial.print(cfg.vpriBottomK, 2);
  CmdSerial.print("k / "); CmdSerial.println(dividerRatio(cfg.vpriTopK, cfg.vpriBottomK), 8);

  CmdSerial.print("Active load slot: "); CmdSerial.println((int)cfg.activeCalLoadSlot + 1);
  for (uint8_t i = 0; i < CAL_LOAD_SLOT_COUNT; i++) {
    CmdSerial.print("LOAD"); CmdSerial.print((int)i + 1);
    CmdSerial.print(": R="); CmdSerial.print(calLoadOhms(i), 3); CmdSerial.print(" ohm");
    if (loadProfileValid(i)) {
      CmdSerial.print(" tuned FEN="); CmdSerial.print(cfg.calLoadFreqHz[i]);
      CmdSerial.print("Hz BIAS="); CmdSerial.print(dutyX10ToPercent(cfg.calLoadDutyX10[i]), 2);
      CmdSerial.print("% BHIGH="); CmdSerial.print(dutyX10ToPercent(cfg.calLoadDutyX10[i]), 2);
      CmdSerial.print(" Pmeas="); CmdSerial.print(cfg.calLoadMeasuredW[i], 3);
      CmdSerial.print(" Vsec="); CmdSerial.print(cfg.calLoadMeasuredVsec[i], 3);
    } else {
      CmdSerial.print(" not tuned");
    }
    CmdSerial.println();
  }

  CmdSerial.print("EEPROM slot/seq: "); CmdSerial.print(activeSlotIndex); CmdSerial.print(" / "); CmdSerial.println(settingsSequence);
  CmdSerial.print("EEPROM pending save: "); CmdSerial.println(settingsDirty ? "YES" : "NO");
  printParams();
  CmdSerial.println("========================================");
}

bool parseSetParam(String name, float value) {
  name.trim();
  name.toUpperCase();

  if (name == "PFBSRC" || name == "PFB") {
    cfg.powerFeedbackMode = (value >= 0.5f) ? (uint8_t)PFB_SECONDARY_VI : (uint8_t)PFB_PRIMARY_VI;
    filtersPrimed = false;
  }
  else if (name == "PTARGET" || name == "PWR" || name == "P") cfg.targetPowerW = clampFloat(value, POWER_TARGET_MIN_W, POWER_TARGET_MAX_W);
  else if (name == "VREF") cfg.adcRefV = clampFloat(value, 1.0f, 3.6f);
  else if (name == "VPRITOP") cfg.vpriTopK = clampFloat(value, 1.0f, 10000.0f);
  else if (name == "VPRIBOT") cfg.vpriBottomK = clampFloat(value, 0.1f, 1000.0f);
  else if (name == "VPRIGAIN") cfg.vpriGain = clampFloat(value, 0.1f, 10.0f);
  else if (name == "VPRIOFF") cfg.vpriOffsetV = clampFloat(value, -100.0f, 100.0f);

  else if (name == "AMCREF") cfg.amcRefV = clampFloat(value, 1.0f, 5.0f);
  else if (name == "AMCVCLIP") cfg.amcVclipV = clampFloat(value, 0.5f, 3.0f);
  else if (name == "VSECTOP") cfg.vsecTopK = clampFloat(value, 1.0f, 10000.0f);
  else if (name == "VSECBOT") cfg.vsecBottomK = clampFloat(value, 0.1f, 1000.0f);
  else if (name == "VSECGAIN") cfg.vsecGain = clampFloat(value, 0.1f, 10.0f);
  else if (name == "VSECOFF") cfg.vsecOffsetV = clampFloat(value, -20.0f, 20.0f);

  else if (name == "CSRES") cfg.csResOhms = clampFloat(value, 1.0f, 10000.0f);
  else if (name == "CSGAIN") cfg.csGainAperA = clampFloat(value, 0.000001f, 0.1f);
  else if (name == "CSOFF") cfg.currentOffsetV = clampFloat(value, -1.0f, 1.0f);
  else if (name == "IABS") cfg.currentAbsMode = (value >= 0.5f) ? 1 : 0;
  else if (name == "ITRIP") cfg.currentTripA = clampFloat(value, 0.1f, 100.0f);
  else if (name == "ITRIPEN") cfg.currentTripEnable = (value >= 0.5f) ? 1 : 0;
  else if (name == "ISOFT") cfg.currentSoftA = clampFloat(value, 0.0f, 100.0f);
  else if (name == "IFOLDEN") cfg.currentFoldbackEnable = (value >= 0.5f) ? 1 : 0;
  else if (name == "IFOLD") cfg.currentFoldPctPerA = clampFloat(value, 0.0f, 100.0f);

  else if (name == "PRECHEN") cfg.prechargeEnable = (value >= 0.5f) ? 1 : 0;
  else if (name == "PREDUTY") cfg.prechargeDutyX10 = dutyPercentToX10(value);
  else if (name == "PREMS") cfg.prechargeBurstMs = clampU32((uint32_t)value, 1UL, 500UL);
  else if (name == "PRESETTLE") cfg.prechargeSettleMs = clampU32((uint32_t)value, 1UL, 2000UL);
  else if (name == "PREMAX") cfg.prechargeMaxBursts = (uint8_t)clampU32((uint32_t)value, 1UL, 20UL);
  else if (name == "PREV") cfg.prechargeReadyV = clampFloat(value, 0.0f, SEC_V_MAX_HARD);
  else if (name == "PREAUTOMAX") cfg.prechargeTuneMaxDutyX10 = dutyPercentToX10(value);
  else if (name == "PRETRIES") cfg.prechargeTuneMaxBursts = (uint8_t)clampU32((uint32_t)value, 1UL, 50UL);

  else if (name == "FEN" || name == "E") cfg.enFreqHz = clampU32((uint32_t)value, cfg.enFreqMinHz, cfg.enFreqMaxHz);
  else if (name == "FMIN") cfg.enFreqMinHz = clampU32((uint32_t)value, EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
  else if (name == "FMAX") cfg.enFreqMaxHz = clampU32((uint32_t)value, EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
  else if (name == "FPREF") cfg.enFreqPrefHz = clampU32((uint32_t)value, EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
  else if (name == "FPEN") cfg.enFreqPenaltyW = clampFloat(value, 0.0f, 1000.0f);
  else if (name == "MINEDGE") cfg.enMinEdgeUs = (uint16_t)clampU32((uint32_t)value, EN_MIN_EDGE_HARD_US, EN_MAX_EDGE_HARD_US);
  else if (name == "GATECYC" || name == "GATEMIN") cfg.enMinGateCycles = (uint16_t)clampU32((uint32_t)value, EN_MIN_GATE_CYCLES_MIN, EN_MIN_GATE_CYCLES_MAX);
  else if (name == "GATELEAD" || name == "GATEWAKE") cfg.enGateLeadCycles = (uint16_t)clampU32((uint32_t)value, EN_GATE_LEAD_CYCLES_MIN, EN_GATE_LEAD_CYCLES_MAX);
  else if (name == "STATIC") cfg.allowStatic100 = (value >= 0.5f) ? 1 : 0;
  else if (name == "DMIN") cfg.dutyMinX10 = dutyPercentToX10(value);
  else if (name == "DMAX") cfg.dutyMaxX10 = dutyPercentToX10(value);
  else if (name == "OD" || name == "D") cfg.openLoopDutyX10 = dutyPercentToX10(value);
  else if (name == "BIAS" || name == "B") {
    cfg.biasDutyX10 = dutyPercentToX10(value);
    cfg.bangHighDutyX10 = cfg.biasDutyX10;
  }
  else if (name == "PWRDUTY") cfg.powerupDutyX10 = dutyPercentToX10(value);
  else if (name == "BLOW") cfg.bangLowDutyX10 = dutyPercentToX10(value);
  else if (name == "BHIGH") {
    cfg.bangHighDutyX10 = dutyPercentToX10(value);
    cfg.biasDutyX10 = cfg.bangHighDutyX10;
  }
  else if (name == "BHYST") cfg.bangHystMw = (int32_t)(clampFloat(value, 0.0f, 1000.0f) * 1000.0f + 0.5f);
  else if (name == "BONMS") cfg.bangMinOnMs = clampU32((uint32_t)value, 0UL, 1000UL);
  else if (name == "BOFFMS") cfg.bangMinOffMs = clampU32((uint32_t)value, 0UL, 1000UL);

  else if (name == "CPER") cfg.controlPeriodUs = clampU32((uint32_t)value, CONTROL_PERIOD_MIN_US, CONTROL_PERIOD_MAX_US);
  else if (name == "STATUSMS") cfg.statusMs = clampU32((uint32_t)value, 100UL, 5000UL);
  else if (name == "ADCVP") cfg.adcVpriSamples = (uint16_t)clampU32((uint32_t)value, 1, 64);
  else if (name == "ADCVS") cfg.adcVsecSamples = (uint16_t)clampU32((uint32_t)value, 1, 64);
  else if (name == "ADCI") cfg.adcISamples = (uint16_t)clampU32((uint32_t)value, 1, 64);
  else if (name == "ADCDUMMY") cfg.adcDummy = (uint16_t)clampU32((uint32_t)value, 0, 8);
  else if (name == "PTAU") cfg.powerTauMs = clampFloat(value, 0.1f, 500.0f);
  else if (name == "VPTAU") cfg.vpriTauMs = clampFloat(value, 0.1f, 500.0f);
  else if (name == "VSTAU") cfg.vsecTauMs = clampFloat(value, 0.1f, 500.0f);
  else if (name == "ITAU") cfg.currentTauMs = clampFloat(value, 0.1f, 500.0f);

  else if (name == "KP") cfg.kp_x1000 = (int32_t)(clampFloat(value, 0.0f, 50.0f) * 1000.0f + 0.5f);
  else if (name == "KI") cfg.ki_x1000 = (int32_t)(clampFloat(value, 0.0f, 200.0f) * 1000.0f + 0.5f);
  else if (name == "DB") cfg.deadbandMw = (int32_t)(clampFloat(value, 0.0f, 100.0f) * 1000.0f + 0.5f);
  else if (name == "SLEW") cfg.slewX10PerSec = (int32_t)(clampFloat(value, 0.1f, 3000.0f) * 10.0f + 0.5f);
  else if (name == "IMIN") cfg.integralMinX10 = (int32_t)(clampFloat(value, -100.0f, 100.0f) * 10.0f);
  else if (name == "IMAX") cfg.integralMaxX10 = (int32_t)(clampFloat(value, -100.0f, 100.0f) * 10.0f);

  else if (name == "VMIN") cfg.secMinV = clampFloat(value, SEC_V_MIN_HARD, SEC_V_MAX_HARD);
  else if (name == "VMAX") cfg.secMaxV = clampFloat(value, SEC_V_MIN_HARD, SEC_V_MAX_HARD);
  else if (name == "OVP") cfg.secOvpV = clampFloat(value, SEC_V_MIN_HARD, SEC_V_MAX_HARD);
  else if (name == "OVPEN") cfg.secOvpEnable = (value >= 0.5f) ? 1 : 0;
  else if (name == "VBOOST") cfg.secLowBoostPctPerV = clampFloat(value, 0.0f, 100.0f);
  else if (name == "VFOLD") cfg.secHighFoldPctPerV = clampFloat(value, 0.0f, 100.0f);
  else if (name == "MAXFAULTEN") cfg.maxDutyFaultEnable = (value >= 0.5f) ? 1 : 0;
  else if (name == "MAXFAULTMS") cfg.maxDutyFaultMs = clampU32((uint32_t)value, 50UL, 10000UL);
  else if (name == "MAXFAULTERR") cfg.maxDutyFaultErrMw = (int32_t)(clampFloat(value, 0.0f, 1000.0f) * 1000.0f + 0.5f);

  else if (name == "AUTOMAX") cfg.autotuneMaxDutyX10 = dutyPercentToX10(value);
  else if (name == "AUTOSTEP") cfg.autotuneCoarseStepX10 = (uint16_t)clampU32((uint32_t)(value * 10.0f + 0.5f), 5, 250);
  else if (name == "AUTOFINE") cfg.autotuneFineStepX10 = (uint16_t)clampU32((uint32_t)(value * 10.0f + 0.5f), 1, 100);
  else if (name == "AUTOSETTLE") cfg.autotuneSettleMs = clampU32((uint32_t)value, 20, 3000);
  else if (name == "AUTOMEAS") cfg.autotuneMeasureMs = clampU32((uint32_t)value, 20, 2000);
  else if (name == "AUTOTEST") cfg.autotuneTestStepX10 = (uint16_t)clampU32((uint32_t)(value * 10.0f + 0.5f), 5, 150);
  else if (name == "AUTOFSTEP") cfg.autotuneFreqStepHz = clampU32((uint32_t)value, 500UL, 10000UL);

  else if (name == "LOAD1") cfg.calLoadOhms[0] = clampFloat(value, 0.0f, 100000.0f);
  else if (name == "LOAD2") cfg.calLoadOhms[1] = clampFloat(value, 0.0f, 100000.0f);
  else if (name == "LOAD3") cfg.calLoadOhms[2] = clampFloat(value, 0.0f, 100000.0f);
  else return false;

  validateSettings();
  setEnFrequencyHz(cfg.enFreqHz);
  if (controlMode == MODE_OPEN_LOOP && !startupPrechargeActive()) setEnDutyX10(cfg.openLoopDutyX10);
  else if (controlMode == MODE_POWER_LOOP && !startupPrechargeActive()) setEnDutyX10(bangBangHigh ? cfg.bangHighDutyX10 : cfg.bangLowDutyX10);
  saveSettings();
  return true;
}

void printSaveStateMessage(const char *doneText) {
  if (settingsDirty) {
    CmdSerial.println("Applied in RAM. EEPROM save pending; OFF or SAVE while output is off will flush it.");
  } else if (doneText != nullptr) {
    CmdSerial.println(doneText);
  }
}

void zeroCurrentOffset() {
  float sum = 0.0f;
  for (int i = 0; i < 64; i++) {
    rawPa2Adc = readAdcDmaChannel(ADC_DMA_I_INDEX);
    rawPa2Voltage = adcCountsToVoltage(rawPa2Adc);
    sum += rawPa2Voltage;
    delay(2);
  }
  cfg.currentOffsetV = sum / 64.0f;
  saveSettings();
  CmdSerial.print("Current offset set to ");
  CmdSerial.print(cfg.currentOffsetV, 5);
  CmdSerial.println(" V");
}

int8_t parseLoadSlotText(String text) {
  text.trim();
  if (text.length() == 0) return (int8_t)cfg.activeCalLoadSlot;
  int slot = text.toInt();
  if (slot < 1 || slot > (int)CAL_LOAD_SLOT_COUNT) return -1;
  return (int8_t)(slot - 1);
}

void printLoadCommandHelp() {
  CmdSerial.println("Use LOAD 1..3, CALLOAD 1..3, AUTOBANG 1..3, CAL3, or SET LOAD1/2/3 ohms.");
}

int8_t waitForLoadGo(uint8_t slot) {
  CmdSerial.println();
  CmdSerial.print("Install LOAD");
  CmdSerial.print((int)slot + 1);
  CmdSerial.print(" = ");
  CmdSerial.print(calLoadOhms(slot), 3);
  CmdSerial.println(" ohm, then type GO. Type SKIP or ABORT instead.");
  CmdSerial.print("> ");

  String line;
  bool loadLastWasCr = false;
  while (true) {
    while (CmdSerial.available()) {
      char c = CmdSerial.read();
      if (c == '\r' || c == '\n') {
        if (c == '\n' && loadLastWasCr) {
          loadLastWasCr = false;
          continue;
        }
        loadLastWasCr = (c == '\r');
        line.trim();
        line.toUpperCase();
        CmdSerial.println();
        if (line == "GO" || line == "G") return 1;
        if (line == "SKIP" || line == "S") return 0;
        if (line == "ABORT" || line == "A" || line == "OFF") return -1;
        CmdSerial.println("Type GO, SKIP, or ABORT.");
        CmdSerial.print("> ");
        line = "";
      } else if (c == 8 || c == 127) {
        loadLastWasCr = false;
        if (line.length() > 0) {
          line.remove(line.length() - 1);
          CmdSerial.print("\b \b");
        }
      } else {
        loadLastWasCr = false;
        line += c;
        CmdSerial.write(c);
      }
    }
    delay(10);
  }
}

void autoTuneThreeLoads() {
  for (uint8_t slot = 0; slot < CAL_LOAD_SLOT_COUNT; slot++) {
    setSystemEnabled(false, true);
    int8_t action = waitForLoadGo(slot);
    if (action < 0) {
      CmdSerial.println("CAL3 aborted.");
      CmdSerial.print("> ");
      return;
    }
    if (action == 0) {
      CmdSerial.print("LOAD");
      CmdSerial.print((int)slot + 1);
      CmdSerial.println(" skipped.");
      continue;
    }
    autoTunePower(true, (int8_t)slot);
    setSystemEnabled(false, true);
  }
  CmdSerial.println("CAL3 complete. Use LOAD 1..3 to apply saved profiles.");
  CmdSerial.print("> ");
}

void processCommand(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;

  String up = cmd;
  up.toUpperCase();

  if (up == "?" || up == "STATUS") { printStatus(); return; }
  if (up == "VER" || up == "VERSION") { CmdSerial.println(FW_VERSION_STRING); return; }
  if (up == "PARAMS") { printParams(); return; }
  if (up == "DIVIDER" || up == "LADDER") { printDividerAdvice(); return; }
  if (up == "AUTOPRE" || up == "PREAUTO" || up == "CALPRE") { autoTunePrecharge(); return; }
  if (up == "ON") { setSystemEnabled(true, false); CmdSerial.println("System ON"); return; }
  if (up == "OFF") { setSystemEnabled(false, true); CmdSerial.println("System OFF"); return; }
  if (up == "OPEN" || up == "MO") { setMode(MODE_OPEN_LOOP, true); CmdSerial.println("OPEN LOOP"); return; }
  if (up == "BANG" || up == "POWER" || up == "MC" || up == "CLOSED") { setMode(MODE_POWER_LOOP, true); CmdSerial.println("BANG-BANG LOOP"); return; }
  if (up == "PFBPRI" || up == "PRIMARYVI" || up == "PRI_V_I") {
    cfg.powerFeedbackMode = (uint8_t)PFB_PRIMARY_VI;
    filtersPrimed = false;
    validateSettings();
    saveSettings();
    printSaveStateMessage("Power feedback source set to PRI_V_I.");
    return;
  }
  if (up == "PFBSEC" || up == "SECVI" || up == "SECONDARYVI" || up == "SEC_V_I") {
    cfg.powerFeedbackMode = (uint8_t)PFB_SECONDARY_VI;
    filtersPrimed = false;
    validateSettings();
    saveSettings();
    printSaveStateMessage("Power feedback source set to SEC_V_I.");
    return;
  }
  if (up == "CAL" || up == "AUTOTUNE" || up == "AUTOFULL" || up == "AUTOBANG") { autoTunePower(true, (int8_t)cfg.activeCalLoadSlot); return; }
  if (up == "CAL3") { autoTuneThreeLoads(); return; }
  if (up == "SAVE") {
    if (requestSettingsSave("manual")) CmdSerial.println("Saved.");
    else CmdSerial.println("Output is active; settings are applied in RAM and EEPROM save is pending. Send OFF to flush safely.");
    return;
  }
  if (up == "DEFAULTS") {
    setSystemEnabled(false, false);
    setDefaults();
    validateSettings();
    controlMode = MODE_OPEN_LOOP;
    systemEnabled = false;
    cfg.systemEnabled = 0;
    cfg.controlMode = MODE_OPEN_LOOP;
    saveSettingsNow();
    setMode(MODE_OPEN_LOOP, false);
    CmdSerial.println("Defaults restored and saved.");
    return;
  }
  if (up == "CLR") { faultLatched = false; faultCode = FAULT_NONE; setGateOutputsEnabled(systemEnabled); updateModeLEDs(); CmdSerial.println("Fault cleared."); return; }
  if (up == "ZEROI" || up == "IZERO") { zeroCurrentOffset(); return; }
  if (up == "FAST") { cfg.controlPeriodUs = 100; cfg.powerTauMs = 1.0f; saveSettings(); printSaveStateMessage("Fast preset saved: CPER=100 us. ADC is DMA-only."); return; }
  if (up == "TURBO") { cfg.controlPeriodUs = 50; cfg.powerTauMs = 0.5f; cfg.vpriTauMs = 0.5f; cfg.currentTauMs = 0.5f; cfg.vsecTauMs = 1.0f; cfg.statusMs = 1000; saveSettings(); printSaveStateMessage("Turbo preset saved: CPER=50 us with DMA-only ADC. Check overruns in STATUS."); return; }
  if (up == "SAFE") { cfg.dutyMaxX10 = 500; cfg.autotuneMaxDutyX10 = 400; cfg.allowStatic100 = 0; cfg.maxDutyFaultEnable = 1; cfg.currentTripEnable = 1; saveSettings(); printSaveStateMessage("Safe preset saved."); return; }

  if (up.startsWith("CALLOAD")) {
    int8_t slot = parseLoadSlotText(up.substring(7));
    if (slot < 0) { printLoadCommandHelp(); return; }
    autoTunePower(true, slot);
    return;
  }

  if (up.startsWith("AUTOBANG") || up.startsWith("AUTOFULL") || up.startsWith("CALFULL")) {
    uint8_t prefixLen = up.startsWith("AUTOBANG") ? 8 : (up.startsWith("AUTOFULL") ? 8 : 7);
    int8_t slot = parseLoadSlotText(up.substring(prefixLen));
    if (slot < 0) { printLoadCommandHelp(); return; }
    autoTunePower(true, slot);
    return;
  }

  if (up.startsWith("LOAD")) {
    int8_t slot = parseLoadSlotText(up.substring(4));
    if (slot < 0) { printLoadCommandHelp(); return; }
    applyLoadProfile((uint8_t)slot, true);
    CmdSerial.print("Active load slot ");
    CmdSerial.print((int)slot + 1);
    CmdSerial.println(loadProfileValid((uint8_t)slot) ? " applied." : " selected, not tuned yet.");
    return;
  }

  if (up.startsWith("SET ")) {
    String rest = cmd.substring(4);
    rest.trim();
    int sp = rest.indexOf(' ');
    if (sp < 0) {
      CmdSerial.println("Use SET NAME VALUE");
      return;
    }
    String name = rest.substring(0, sp);
    String val = rest.substring(sp + 1);
    float f = val.toFloat();
    if (parseSetParam(name, f)) {
      CmdSerial.print("Set ");
      CmdSerial.print(name);
      CmdSerial.print(" = ");
      CmdSerial.println(f, 6);
      if (settingsDirty) CmdSerial.println("EEPROM save pending until output is OFF.");
    } else {
      CmdSerial.println("Unknown parameter. Type PARAMS.");
    }
    return;
  }

  // Short aliases
  if (up.startsWith("P ")) { if (parseSetParam("PTARGET", cmd.substring(2).toFloat())) printSaveStateMessage("Power target saved."); return; }
  if (up.startsWith("D ")) { if (parseSetParam("OD", cmd.substring(2).toFloat())) printSaveStateMessage("Open-loop duty saved."); return; }
  if (up.startsWith("F ")) { if (parseSetParam("FEN", cmd.substring(2).toFloat())) printSaveStateMessage("EN frequency saved."); return; }

  CmdSerial.println("Unknown command. Type ? or PARAMS.");
}

void handleSerial() {
  if (millis() - lastUartCharMs > 5000UL && inputLen == 0) uartInputActive = false;

  uint8_t budget = systemEnabled ? UART_BYTES_PER_LOOP_ACTIVE : UART_BYTES_PER_LOOP_IDLE;
  while (CmdSerial.available() && budget > 0) {
    budget--;
    char c = CmdSerial.read();
    lastUartCharMs = millis();
    uartInputActive = true;

    if (c == '\r' || c == '\n') {
      if (c == '\n' && lastSerialWasCr) {
        lastSerialWasCr = false;
        continue;
      }
      lastSerialWasCr = (c == '\r');
      CmdSerial.println();
      CmdSerial.print("> ");
      inputLine[inputLen] = '\0';
      String cmd(inputLine);
      inputLen = 0;
      inputLine[0] = '\0';
      if (cmd.length()) processCommand(cmd);
      CmdSerial.print("> ");
    } else if (c == 8 || c == 127) {
      lastSerialWasCr = false;
      if (inputLen > 0) {
        inputLen--;
        inputLine[inputLen] = '\0';
        CmdSerial.print("\b \b");
      }
    } else {
      lastSerialWasCr = false;
      if (inputLen < UART_INPUT_MAX_CHARS) {
        inputLine[inputLen++] = c;
        inputLine[inputLen] = '\0';
        CmdSerial.write(c);
      }
    }
  }
}

// ============================================================
// Arduino setup / loop
// ============================================================

void setup() {
  CmdSerial.begin(CMD_UART_BAUD);
  delay(250);

  pinMode(LED_OPEN_PIN, OUTPUT);
  pinMode(LED_CLOSED_PIN, OUTPUT);
  pinMode(LED_SYS_PIN, OUTPUT);
  ledWrite(LED_OPEN_PIN, false);
  ledWrite(LED_CLOSED_PIN, false);
  ledWrite(LED_SYS_PIN, false);

  pinMode(SENSE_VPRI_PIN, INPUT_ANALOG);
  pinMode(SENSE_VOUT_PIN, INPUT_ANALOG);
  pinMode(SENSE_CURRENT_PIN, INPUT_ANALOG);

  analogWriteResolution(12);

  EEPROM.begin();
  loadSettings();

  if (!setupAdcDma()) {
    faultLatched = true;
    faultCode = FAULT_SENSOR;
    systemEnabled = false;
    cfg.systemEnabled = 0;
    CmdSerial.println("ERROR: ADC1 DMA setup failed. Analog feedback disabled; output held off.");
  }

  setupGatePWM();
  setupEnablePWM();
  applyLoadProfile(cfg.activeCalLoadSlot, false);
  setGateOutputsEnabled(systemEnabled);
  if (systemEnabled) runStartupPrechargeBlocking();
  else setEnDutyX10(0);
  updateModeLEDs();

  for (uint8_t i = 0; i < 10; i++) {
    updateAnalogFilters(true);
    delay(2);
  }

  CmdSerial.println();
  CmdSerial.println("STM32G071 primary-power controller loaded");
  CmdSerial.print("Firmware "); CmdSerial.println(FW_VERSION_STRING);
  CmdSerial.println("PA8/PA9 fixed 1 MHz. PA10 EN uses fixed-frequency bang-bang throttle, default 10 kHz.");
  CmdSerial.println("Default feedback: PA1 secondary voltage * PA2 secondary-current signal. PA0 is diagnostic/optional.");
  CmdSerial.println("Type ? for status, VER for version.");
  printDividerAdvice();
  printStatus();
  CmdSerial.print("> ");
}

void loop() {
  handleSerial();

  if (systemEnabled && !autoTuneRunning) {
    if (!handleStartupPrecharge()) {
      handlePowerLoop();
    }
  }

  static uint32_t lastBgUs = 0;
  uint32_t nowUs = micros();
  if (!autoTuneRunning && !startupPrechargeActive() && nowUs - lastBgUs >= 2000UL) {
    lastBgUs = nowUs;
    if (!systemEnabled || controlMode == MODE_OPEN_LOOP) {
      updateAnalogFilters(true);
      checkFaults();
    }
  }

  static uint32_t lastStatus = 0;
  if (!uartInputActive && !autoTuneRunning && millis() - lastStatus >= cfg.statusMs) {
    lastStatus = millis();
    printLiveStatusLine();
  }

  if (settingsDirty && !uartInputActive && !systemEnabled && !autoTuneRunning &&
      !startupPrechargeActive() && millis() - settingsDirtyMs >= EEPROM_DEFER_QUIET_MS) {
    flushPendingSettingsSave(true);
  }
}
