#include <Arduino.h>
#include <EEPROM.h>
#include <math.h>
#include <string.h>

// ============================================================
// STM32G071 LLC / GaN closed-loop burst firmware
// Fixed: PA8/PA9 1 MHz complementary-ish 50% gate drive with requested 40 ns skew.
// Closed-loop actuators: PA10 EN duty and PA10 EN burst frequency only.
// Feedback paths selectable by UART:
//   FB 0 = secondary voltage only, ADC on PA1
//   FB 1 = secondary voltage + primary half-bridge current foldback, ADC PA1 + PA2
//   FB 2 = isolated comparator path on PA1 using COMP1 + DAC1_CH1 threshold
//   FB 3 = comparator path + primary current foldback
// ============================================================

// -------------------- Pins --------------------
#define HIGH_GATE_PIN PA8
#define LOW_GATE_PIN  PA9
#define EN_PIN        PA10

#define SENSE_VOUT_PIN    PA1
#define SENSE_CURRENT_PIN PA2
#define COMP_DAC_PIN      PA4   // DAC1_CH1 used internally as COMP1 minus threshold

#define LED_OPEN_PIN   PB13
#define LED_CLOSED_PIN PB14
#define LED_SYS_PIN    PB15

// Command UART selection:
//   0 = explicit HardwareSerial on PC5 RX / PC4 TX.
// Keep this at 0 for the external isolated command UART and to leave PA2 free
// for half-bridge current sensing.
#define CMD_UART_USE_ARDUINO_SERIAL 0
#define CMD_UART_SERIAL_USES_PA2    1
#define CMD_UART_BAUD               115200UL
#define CMD_UART_EXTERNAL_RX_PIN    PC5
#define CMD_UART_EXTERNAL_TX_PIN    PC4

#if CMD_UART_USE_ARDUINO_SERIAL
#define CmdSerial Serial
#else
HardwareSerial CmdSerial(CMD_UART_EXTERNAL_RX_PIN, CMD_UART_EXTERNAL_TX_PIN); // RX, TX
#endif

// -------------------- Fixed gate settings --------------------
#define GATE_FREQ_HZ       1000000UL
#define GATE_DEADTIME_NS   40UL

// Keep the fixed PA8/PA9 carrier alive once TIM1 is initialized.
// Faults, OFF, and closed-loop limiting shut power transfer down by
// pulling PA10 EN low; they do not block the 1 MHz gate PWM carrier.
#define KEEP_GATE_PWM_RUNNING 1

// -------------------- Hard compile-time limits --------------------
#define ADC_RESOLUTION_BITS 12
#define ADC_MAX_COUNTS      ((1UL << ADC_RESOLUTION_BITS) - 1UL)

#define EN_FREQ_MIN_HARD_HZ    1000UL
#define EN_FREQ_MAX_HARD_HZ   50000UL
#define EN_MIN_EDGE_HARD_US       1UL
#define EN_MAX_EDGE_HARD_US      20UL

#define TARGET_MIN_V           0.5f
#define TARGET_MAX_V          32.0f
#define DUTY_X10_MIN             0
#define DUTY_X10_MAX          1000

#define EEPROM_MAGIC       0x4C4C4338UL
#define EEPROM_SLOT_COUNT  4
#define EEPROM_BASE_ADDR   0

#define LED_ACTIVE_LOW false

// -------------------- Defaults --------------------
#define DEFAULT_SYSTEM_ENABLED      0
#define DEFAULT_CONTROL_MODE        MODE_OPEN_LOOP
#define DEFAULT_FEEDBACK_PATH       FB_SECONDARY_VOLTAGE

#define DEFAULT_ADC_REF_V           3.300f
#define DEFAULT_AMC_REFIN_V         3.300f
#define DEFAULT_AMC_VCLIP_V         1.280f
#define DEFAULT_VDIV_TOP_K          390.0f
#define DEFAULT_VDIV_BOTTOM_K        10.0f

#define DEFAULT_CS_RES_OHMS         820.0f
#define DEFAULT_CS_GAIN_A_PER_A       0.000901f

#define DEFAULT_TARGET_V             12.000f
#define DEFAULT_EN_FREQ_HZ        10000UL
#define DEFAULT_EN_FREQ_MIN_HZ     2000UL
#define DEFAULT_EN_FREQ_MAX_HZ    50000UL
#define DEFAULT_EN_MIN_EDGE_US        2UL

#define DEFAULT_OPEN_DUTY_X10         0
#define DEFAULT_BIAS_DUTY_X10       100   // 10.0%
#define DEFAULT_POWERUP_DUTY_X10    120   // 12.0%
#define DEFAULT_DUTY_MIN_X10          0
#define DEFAULT_DUTY_MAX_X10        950   // closed-loop/open-loop clamp; avoids accidental 100%
#define DEFAULT_ALLOW_STATIC_100      0   // 0 keeps a real low pulse on PA10 even if commanded 100%

#define CONTROL_PERIOD_MIN_HARD_US  100UL
#define CONTROL_PERIOD_MAX_HARD_US 20000UL
#define DEFAULT_CONTROL_PERIOD_US   250UL // 4 kHz request; actual rate/overruns printed in status
#define DEFAULT_STATUS_MS          500UL
#define DEFAULT_ADC_V_SAMPLES         3
#define DEFAULT_ADC_I_SAMPLES         2
#define DEFAULT_ADC_DUMMY             1
#define DEFAULT_VOUT_TAU_MS           3.0f
#define DEFAULT_CURRENT_TAU_MS        2.0f
#define DEFAULT_SENSOR_MIN_PA1_V      0.20f

#define DEFAULT_KP_X1000           1000L  // 1.000 %/V
#define DEFAULT_KI_X1000          12000L  // 12.000 %/(V*s)
#define DEFAULT_DEADBAND_MV          30L
#define DEFAULT_SLEW_X10_PER_SEC   2500L  // 250.0 %/s
#define DEFAULT_INT_MIN_X10        -500L
#define DEFAULT_INT_MAX_X10         500L

#define DEFAULT_CURRENT_TRIP_ENABLE   1
#define DEFAULT_CURRENT_TRIP_A        5.50f
#define DEFAULT_CURRENT_SOFT_A        4.50f
#define DEFAULT_CURRENT_FOLDBACK_EN   1
#define DEFAULT_CURRENT_FOLD_PCT_A   18.0f  // duty percent removed per amp above soft limit
#define DEFAULT_CURRENT_DROOP_V_A     0.00f // target droop per amp, default disabled

#define DEFAULT_MAX_DUTY_FAULT_EN     0
#define DEFAULT_MAX_DUTY_FAULT_MS  1000UL
#define DEFAULT_MAX_DUTY_ERR_MV      800L
#define DEFAULT_OVP_V                30.0f
#define DEFAULT_OVP_ENABLE            1

#define DEFAULT_COMP_RAMP_UP_X10_S  1800L // 180.0 %/s up
#define DEFAULT_COMP_RAMP_DN_X10_S  2200L // 220.0 %/s down
#define DEFAULT_COMP_DAC_OFFSET_MV     0L
#define DEFAULT_COMP_HYST_CODE          2  // 0 none, 1 low, 2 medium, 3 high

#define DEFAULT_AUTOTUNE_MAX_DUTY_X10  950
#define DEFAULT_AUTOTUNE_COARSE_X10     50
#define DEFAULT_AUTOTUNE_BINARY_STEPS    7
#define DEFAULT_AUTOTUNE_SETTLE_MS     250UL
#define DEFAULT_AUTOTUNE_MEASURE_MS    120UL
#define DEFAULT_AUTOTUNE_STEP_X10       30

#define CAL_LOAD_SLOT_COUNT              3
#define DEFAULT_CAL_LOAD1_OHMS          10.0f
#define DEFAULT_CAL_LOAD2_OHMS           5.0f
#define DEFAULT_CAL_LOAD3_OHMS           2.5f

// ============================================================
// Types
// ============================================================

enum ControlMode : uint8_t {
  MODE_OPEN_LOOP = 0,
  MODE_CLOSED_LOOP = 1
};

enum FeedbackPath : uint8_t {
  FB_SECONDARY_VOLTAGE = 0,
  FB_VOLTAGE_CURRENT = 1,
  FB_COMPARATOR = 2,
  FB_COMPARATOR_CURRENT = 3
};

enum FaultCode : uint8_t {
  FAULT_NONE = 0,
  FAULT_CURRENT = 1,
  FAULT_OVP = 2,
  FAULT_SENSOR = 3,
  FAULT_MAX_DUTY = 4
};

struct __attribute__((packed)) SettingsSlot {
  uint32_t magic;
  uint32_t sequence;

  uint8_t systemEnabled;
  uint8_t controlMode;
  uint8_t feedbackPath;
  uint8_t allowStatic100;

  uint16_t openLoopDutyX10;
  uint16_t biasDutyX10;
  uint16_t powerupDutyX10;
  uint16_t dutyMinX10;
  uint16_t dutyMaxX10;

  uint32_t enFreqHz;
  uint32_t enFreqMinHz;
  uint32_t enFreqMaxHz;
  uint32_t controlPeriodUs;
  uint32_t statusMs;
  uint32_t maxDutyFaultMs;

  uint16_t enMinEdgeUs;
  uint16_t adcVSamples;
  uint16_t adcISamples;
  uint16_t adcDummy;

  float adcRefV;
  float amcRefV;
  float amcVclipV;
  float vdivTopK;
  float vdivBottomK;
  float voutGain;
  float voutOffsetV;
  float sensorMinPa1V;
  float voutTauMs;
  float currentTauMs;

  float csResOhms;
  float csGainAperA;
  float currentOffsetV;
  float currentTripA;
  float currentSoftA;
  float currentFoldPctPerA;
  float currentDroopVPerA;
  uint8_t currentTripEnable;
  uint8_t currentFoldbackEnable;

  float targetV;
  int32_t kp_x1000;
  int32_t ki_x1000;
  int32_t deadbandMv;
  int32_t slewX10PerSec;
  int32_t integralMinX10;
  int32_t integralMaxX10;

  uint8_t ovpEnable;
  float ovpV;
  uint8_t maxDutyFaultEnable;
  int32_t maxDutyFaultErrMv;

  int32_t compRampUpX10PerSec;
  int32_t compRampDownX10PerSec;
  int32_t compDacOffsetMv;
  uint8_t compHystCode;

  uint16_t autotuneMaxDutyX10;
  uint16_t autotuneCoarseStepX10;
  uint8_t autotuneBinarySteps;
  uint32_t autotuneSettleMs;
  uint32_t autotuneMeasureMs;
  uint16_t autotuneTestStepX10;

  float tunedPlantGainVPerPct;
  float tunedPlantTauS;
  uint16_t tunedDutyX10;
  float tunedTargetV;

  uint8_t activeCalLoadSlot;
  float calLoadOhms[CAL_LOAD_SLOT_COUNT];
  uint32_t calLoadFreqHz[CAL_LOAD_SLOT_COUNT];
  uint16_t calLoadDutyX10[CAL_LOAD_SLOT_COUNT];
  int32_t calLoadKp_x1000[CAL_LOAD_SLOT_COUNT];
  int32_t calLoadKi_x1000[CAL_LOAD_SLOT_COUNT];
  float calLoadGainVPerPct[CAL_LOAD_SLOT_COUNT];
  float calLoadTauS[CAL_LOAD_SLOT_COUNT];
  float calLoadTargetV[CAL_LOAD_SLOT_COUNT];
  float calLoadMeasuredV[CAL_LOAD_SLOT_COUNT];
  float calLoadMeasuredI[CAL_LOAD_SLOT_COUNT];

  uint32_t checksum;
};

struct MeasureResult {
  float avgV;
  float minV;
  float maxV;
  float avgI;
  float avgPa1;
  float avgPa2;
  uint16_t avgAdc1;
  uint16_t avgAdc2;
  uint32_t count;
  uint32_t avgBlockUs;
  bool valid;
  bool sat;
  bool fault;
};

// ============================================================
// Globals
// ============================================================

SettingsSlot cfg;
uint32_t settingsSequence = 0;
int activeSlotIndex = -1;

void saveSettings();
void setEnFrequencyHz(uint32_t hz);
void setEnDutyX10(uint16_t dutyX10);

HardwareTimer *EnTimer = new HardwareTimer(TIM3);

volatile uint16_t enDutyCmdX10 = DEFAULT_OPEN_DUTY_X10;
volatile uint16_t enDutyEffX10 = DEFAULT_OPEN_DUTY_X10;
volatile uint32_t enFreqRuntimeHz = DEFAULT_EN_FREQ_HZ;
volatile uint32_t enPeriodUs = 100;
volatile uint32_t enHighUs = 0;
volatile bool enPwmStateHigh = false;
uint32_t enTimerAppliedPeriodUs = 0;
uint32_t enTimerAppliedHighUs = 0;

ControlMode controlMode = MODE_OPEN_LOOP;
FeedbackPath feedbackPath = FB_SECONDARY_VOLTAGE;

bool systemEnabled = false;
bool faultLatched = false;
FaultCode faultCode = FAULT_NONE;
bool autoTuneRunning = false;
bool uartInputActive = false;
bool comparatorConfigured = false;

float filteredVout = 0.0f;
float filteredCurrent = 0.0f;
float latestVoutRaw = 0.0f;
float latestCurrentRaw = 0.0f;
bool filtersPrimed = false;
bool latestSensorValid = false;
bool latestSensorSaturated = false;

uint16_t rawPa1Adc = 0;
uint16_t rawPa2Adc = 0;
float rawPa1Voltage = 0.0f;
float rawPa2Voltage = 0.0f;

uint32_t lastAnalogUs = 0;
uint32_t lastAdcBlockUs = 0;
uint32_t maxAdcBlockUs = 0;
uint32_t lastControlDtUs = 0;
uint32_t maxControlDtUs = 0;
uint32_t controlOverrunCount = 0;

float controlDutyPercent = 0.0f;
float closedLoopIntegratorPct = 0.0f;
float comparatorDutyX10 = 0.0f;
uint32_t maxDutyStartMs = 0;

bool sensorPowerupActive = false;
uint32_t sensorPowerupStartMs = 0;
uint16_t sensorPowerupDutyActiveX10 = DEFAULT_POWERUP_DUTY_X10;

uint16_t compDacCode = 0;
bool compDacWritten = false;
bool compLastAbove = false;

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

float expectedLoadCurrentA(uint8_t slot) {
  float r = calLoadOhms(slot);
  if (r <= 0.0f) return 0.0f;
  return cfg.targetV / r;
}

float expectedLoadPowerW(uint8_t slot) {
  float r = calLoadOhms(slot);
  if (r <= 0.0f) return 0.0f;
  return (cfg.targetV * cfg.targetV) / r;
}

bool loadProfileValid(uint8_t slot) {
  if (!validLoadSlot(slot)) return false;
  return cfg.calLoadTargetV[slot] > 0.0f &&
         cfg.calLoadFreqHz[slot] >= EN_FREQ_MIN_HARD_HZ &&
         cfg.calLoadDutyX10[slot] > 0;
}

void applyLoadProfile(uint8_t slot, bool save) {
  if (!validLoadSlot(slot)) return;
  cfg.activeCalLoadSlot = slot;

  if (loadProfileValid(slot)) {
    cfg.enFreqHz = cfg.calLoadFreqHz[slot];
    cfg.biasDutyX10 = cfg.calLoadDutyX10[slot];
    cfg.tunedDutyX10 = cfg.calLoadDutyX10[slot];
    cfg.tunedTargetV = cfg.calLoadTargetV[slot];
    cfg.tunedPlantGainVPerPct = cfg.calLoadGainVPerPct[slot];
    cfg.tunedPlantTauS = cfg.calLoadTauS[slot];
    cfg.kp_x1000 = cfg.calLoadKp_x1000[slot];
    cfg.ki_x1000 = cfg.calLoadKi_x1000[slot];
    setEnFrequencyHz(cfg.enFreqHz);
    if (controlMode == MODE_OPEN_LOOP) setEnDutyX10(cfg.openLoopDutyX10);
  }

  if (save) saveSettings();
}

void storeLoadProfile(uint8_t slot, uint32_t freqHz, uint16_t dutyX10,
                      float gainVPerPct, float tauS, float measuredV,
                      float measuredI) {
  if (!validLoadSlot(slot)) return;
  cfg.activeCalLoadSlot = slot;
  cfg.calLoadFreqHz[slot] = clampU32(freqHz, EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
  cfg.calLoadDutyX10[slot] = clampDutyX10(dutyX10);
  cfg.calLoadKp_x1000[slot] = cfg.kp_x1000;
  cfg.calLoadKi_x1000[slot] = cfg.ki_x1000;
  cfg.calLoadGainVPerPct[slot] = gainVPerPct;
  cfg.calLoadTauS[slot] = tauS;
  cfg.calLoadTargetV[slot] = cfg.targetV;
  cfg.calLoadMeasuredV[slot] = measuredV;
  cfg.calLoadMeasuredI[slot] = measuredI;
}

const char *commandUartName() {
#if CMD_UART_USE_ARDUINO_SERIAL
  return "Arduino Serial / ST-LINK VCP";
#else
  return "external UART PC5 RX / PC4 TX";
#endif
}

bool currentSenseAvailable() {
#if CMD_UART_USE_ARDUINO_SERIAL && CMD_UART_SERIAL_USES_PA2
  return false;
#else
  return true;
#endif
}

bool feedbackConfiguredForCurrent() {
  return feedbackPath == FB_VOLTAGE_CURRENT || feedbackPath == FB_COMPARATOR_CURRENT;
}

bool feedbackUsesCurrent() {
  return currentSenseAvailable() && feedbackConfiguredForCurrent();
}

bool currentProtectionEnabled() {
  return currentSenseAvailable() && cfg.currentTripEnable;
}

bool feedbackUsesComparator() {
  return feedbackPath == FB_COMPARATOR || feedbackPath == FB_COMPARATOR_CURRENT;
}

bool feedbackUsesVoltagePid() {
  return feedbackPath == FB_SECONDARY_VOLTAGE || feedbackPath == FB_VOLTAGE_CURRENT;
}

void ledWrite(uint8_t pin, bool on) {
  if (LED_ACTIVE_LOW) digitalWrite(pin, on ? LOW : HIGH);
  else digitalWrite(pin, on ? HIGH : LOW);
}

void updateModeLEDs() {
  ledWrite(LED_OPEN_PIN, systemEnabled && controlMode == MODE_OPEN_LOOP && !faultLatched);
  ledWrite(LED_CLOSED_PIN, systemEnabled && controlMode == MODE_CLOSED_LOOP && !faultLatched);
  ledWrite(LED_SYS_PIN, systemEnabled && !faultLatched);
}

uint32_t getTimerClockHz() {
  SystemCoreClockUpdate();
  return SystemCoreClock;
}

// ============================================================
// Defaults / validation
// ============================================================

void setDefaults() {
  memset(&cfg, 0, sizeof(cfg));
  cfg.magic = EEPROM_MAGIC;
  cfg.sequence = 0;

  cfg.systemEnabled = DEFAULT_SYSTEM_ENABLED;
  cfg.controlMode = (uint8_t)DEFAULT_CONTROL_MODE;
  cfg.feedbackPath = (uint8_t)DEFAULT_FEEDBACK_PATH;
  cfg.allowStatic100 = DEFAULT_ALLOW_STATIC_100;

  cfg.openLoopDutyX10 = DEFAULT_OPEN_DUTY_X10;
  cfg.biasDutyX10 = DEFAULT_BIAS_DUTY_X10;
  cfg.powerupDutyX10 = DEFAULT_POWERUP_DUTY_X10;
  cfg.dutyMinX10 = DEFAULT_DUTY_MIN_X10;
  cfg.dutyMaxX10 = DEFAULT_DUTY_MAX_X10;

  cfg.enFreqHz = DEFAULT_EN_FREQ_HZ;
  cfg.enFreqMinHz = DEFAULT_EN_FREQ_MIN_HZ;
  cfg.enFreqMaxHz = DEFAULT_EN_FREQ_MAX_HZ;
  cfg.controlPeriodUs = DEFAULT_CONTROL_PERIOD_US;
  cfg.statusMs = DEFAULT_STATUS_MS;
  cfg.maxDutyFaultMs = DEFAULT_MAX_DUTY_FAULT_MS;
  cfg.enMinEdgeUs = DEFAULT_EN_MIN_EDGE_US;

  cfg.adcVSamples = DEFAULT_ADC_V_SAMPLES;
  cfg.adcISamples = DEFAULT_ADC_I_SAMPLES;
  cfg.adcDummy = DEFAULT_ADC_DUMMY;

  cfg.adcRefV = DEFAULT_ADC_REF_V;
  cfg.amcRefV = DEFAULT_AMC_REFIN_V;
  cfg.amcVclipV = DEFAULT_AMC_VCLIP_V;
  cfg.vdivTopK = DEFAULT_VDIV_TOP_K;
  cfg.vdivBottomK = DEFAULT_VDIV_BOTTOM_K;
  cfg.voutGain = 1.0f;
  cfg.voutOffsetV = 0.0f;
  cfg.sensorMinPa1V = DEFAULT_SENSOR_MIN_PA1_V;
  cfg.voutTauMs = DEFAULT_VOUT_TAU_MS;
  cfg.currentTauMs = DEFAULT_CURRENT_TAU_MS;

  cfg.csResOhms = DEFAULT_CS_RES_OHMS;
  cfg.csGainAperA = DEFAULT_CS_GAIN_A_PER_A;
  cfg.currentOffsetV = 0.0f;
  cfg.currentTripA = DEFAULT_CURRENT_TRIP_A;
  cfg.currentSoftA = DEFAULT_CURRENT_SOFT_A;
  cfg.currentFoldPctPerA = DEFAULT_CURRENT_FOLD_PCT_A;
  cfg.currentDroopVPerA = DEFAULT_CURRENT_DROOP_V_A;
  cfg.currentTripEnable = DEFAULT_CURRENT_TRIP_ENABLE;
  cfg.currentFoldbackEnable = DEFAULT_CURRENT_FOLDBACK_EN;

  cfg.targetV = DEFAULT_TARGET_V;
  cfg.kp_x1000 = DEFAULT_KP_X1000;
  cfg.ki_x1000 = DEFAULT_KI_X1000;
  cfg.deadbandMv = DEFAULT_DEADBAND_MV;
  cfg.slewX10PerSec = DEFAULT_SLEW_X10_PER_SEC;
  cfg.integralMinX10 = DEFAULT_INT_MIN_X10;
  cfg.integralMaxX10 = DEFAULT_INT_MAX_X10;

  cfg.ovpEnable = DEFAULT_OVP_ENABLE;
  cfg.ovpV = DEFAULT_OVP_V;
  cfg.maxDutyFaultEnable = DEFAULT_MAX_DUTY_FAULT_EN;
  cfg.maxDutyFaultErrMv = DEFAULT_MAX_DUTY_ERR_MV;

  cfg.compRampUpX10PerSec = DEFAULT_COMP_RAMP_UP_X10_S;
  cfg.compRampDownX10PerSec = DEFAULT_COMP_RAMP_DN_X10_S;
  cfg.compDacOffsetMv = DEFAULT_COMP_DAC_OFFSET_MV;
  cfg.compHystCode = DEFAULT_COMP_HYST_CODE;

  cfg.autotuneMaxDutyX10 = DEFAULT_AUTOTUNE_MAX_DUTY_X10;
  cfg.autotuneCoarseStepX10 = DEFAULT_AUTOTUNE_COARSE_X10;
  cfg.autotuneBinarySteps = DEFAULT_AUTOTUNE_BINARY_STEPS;
  cfg.autotuneSettleMs = DEFAULT_AUTOTUNE_SETTLE_MS;
  cfg.autotuneMeasureMs = DEFAULT_AUTOTUNE_MEASURE_MS;
  cfg.autotuneTestStepX10 = DEFAULT_AUTOTUNE_STEP_X10;

  cfg.tunedPlantGainVPerPct = 0.0f;
  cfg.tunedPlantTauS = 0.0f;
  cfg.tunedDutyX10 = DEFAULT_BIAS_DUTY_X10;
  cfg.tunedTargetV = 0.0f;

  cfg.activeCalLoadSlot = 0;
  cfg.calLoadOhms[0] = DEFAULT_CAL_LOAD1_OHMS;
  cfg.calLoadOhms[1] = DEFAULT_CAL_LOAD2_OHMS;
  cfg.calLoadOhms[2] = DEFAULT_CAL_LOAD3_OHMS;
  for (uint8_t i = 0; i < CAL_LOAD_SLOT_COUNT; i++) {
    cfg.calLoadFreqHz[i] = DEFAULT_EN_FREQ_HZ;
    cfg.calLoadDutyX10[i] = DEFAULT_BIAS_DUTY_X10;
    cfg.calLoadKp_x1000[i] = DEFAULT_KP_X1000;
    cfg.calLoadKi_x1000[i] = DEFAULT_KI_X1000;
    cfg.calLoadGainVPerPct[i] = 0.0f;
    cfg.calLoadTauS[i] = 0.0f;
    cfg.calLoadTargetV[i] = 0.0f;
    cfg.calLoadMeasuredV[i] = 0.0f;
    cfg.calLoadMeasuredI[i] = 0.0f;
  }
}

void validateSettings() {
  if (cfg.magic != EEPROM_MAGIC) setDefaults();

  cfg.systemEnabled = cfg.systemEnabled ? 1 : 0;
  if (cfg.controlMode > MODE_CLOSED_LOOP) cfg.controlMode = MODE_OPEN_LOOP;
  if (cfg.feedbackPath > FB_COMPARATOR_CURRENT) cfg.feedbackPath = FB_SECONDARY_VOLTAGE;
  cfg.allowStatic100 = cfg.allowStatic100 ? 1 : 0;

  cfg.openLoopDutyX10 = clampDutyX10(cfg.openLoopDutyX10);
  cfg.biasDutyX10 = clampDutyX10(cfg.biasDutyX10);
  cfg.powerupDutyX10 = clampDutyX10(cfg.powerupDutyX10);
  cfg.dutyMinX10 = clampDutyX10(cfg.dutyMinX10);
  cfg.dutyMaxX10 = clampDutyX10(cfg.dutyMaxX10);
  if (cfg.dutyMaxX10 < cfg.dutyMinX10 + 10) cfg.dutyMaxX10 = cfg.dutyMinX10 + 10;
  if (cfg.dutyMaxX10 > DUTY_X10_MAX) cfg.dutyMaxX10 = DUTY_X10_MAX;

  cfg.enFreqMinHz = clampU32(cfg.enFreqMinHz, EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
  cfg.enFreqMaxHz = clampU32(cfg.enFreqMaxHz, EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
  if (cfg.enFreqMaxHz < cfg.enFreqMinHz) cfg.enFreqMaxHz = cfg.enFreqMinHz;
  cfg.enFreqHz = clampU32(cfg.enFreqHz, cfg.enFreqMinHz, cfg.enFreqMaxHz);
  cfg.enMinEdgeUs = (uint16_t)clampU32(cfg.enMinEdgeUs, EN_MIN_EDGE_HARD_US, EN_MAX_EDGE_HARD_US);

  cfg.controlPeriodUs = clampU32(cfg.controlPeriodUs, CONTROL_PERIOD_MIN_HARD_US, CONTROL_PERIOD_MAX_HARD_US);
  cfg.statusMs = clampU32(cfg.statusMs, 100UL, 5000UL);
  cfg.maxDutyFaultMs = clampU32(cfg.maxDutyFaultMs, 50UL, 10000UL);

  cfg.adcVSamples = (uint16_t)clampU32(cfg.adcVSamples, 1, 64);
  cfg.adcISamples = (uint16_t)clampU32(cfg.adcISamples, 1, 64);
  cfg.adcDummy = (uint16_t)clampU32(cfg.adcDummy, 0, 8);

  if (!isfinite(cfg.adcRefV) || cfg.adcRefV < 1.0f || cfg.adcRefV > 3.6f) cfg.adcRefV = DEFAULT_ADC_REF_V;
  if (!isfinite(cfg.amcRefV) || cfg.amcRefV < 1.0f || cfg.amcRefV > 5.0f) cfg.amcRefV = DEFAULT_AMC_REFIN_V;
  if (!isfinite(cfg.amcVclipV) || cfg.amcVclipV < 0.5f || cfg.amcVclipV > 3.0f) cfg.amcVclipV = DEFAULT_AMC_VCLIP_V;
  if (!isfinite(cfg.vdivTopK) || cfg.vdivTopK < 1.0f || cfg.vdivTopK > 10000.0f) cfg.vdivTopK = DEFAULT_VDIV_TOP_K;
  if (!isfinite(cfg.vdivBottomK) || cfg.vdivBottomK < 0.1f || cfg.vdivBottomK > 1000.0f) cfg.vdivBottomK = DEFAULT_VDIV_BOTTOM_K;
  if (!isfinite(cfg.voutGain) || cfg.voutGain < 0.1f || cfg.voutGain > 10.0f) cfg.voutGain = 1.0f;
  if (!isfinite(cfg.voutOffsetV) || cfg.voutOffsetV < -20.0f || cfg.voutOffsetV > 20.0f) cfg.voutOffsetV = 0.0f;
  if (!isfinite(cfg.sensorMinPa1V) || cfg.sensorMinPa1V < 0.0f || cfg.sensorMinPa1V > 2.0f) cfg.sensorMinPa1V = DEFAULT_SENSOR_MIN_PA1_V;
  if (!isfinite(cfg.voutTauMs) || cfg.voutTauMs < 0.1f || cfg.voutTauMs > 500.0f) cfg.voutTauMs = DEFAULT_VOUT_TAU_MS;
  if (!isfinite(cfg.currentTauMs) || cfg.currentTauMs < 0.1f || cfg.currentTauMs > 500.0f) cfg.currentTauMs = DEFAULT_CURRENT_TAU_MS;

  if (!isfinite(cfg.csResOhms) || cfg.csResOhms < 1.0f || cfg.csResOhms > 10000.0f) cfg.csResOhms = DEFAULT_CS_RES_OHMS;
  if (!isfinite(cfg.csGainAperA) || cfg.csGainAperA < 0.000001f || cfg.csGainAperA > 0.1f) cfg.csGainAperA = DEFAULT_CS_GAIN_A_PER_A;
  if (!isfinite(cfg.currentOffsetV) || cfg.currentOffsetV < -1.0f || cfg.currentOffsetV > 1.0f) cfg.currentOffsetV = 0.0f;
  if (!isfinite(cfg.currentTripA) || cfg.currentTripA < 0.1f || cfg.currentTripA > 100.0f) cfg.currentTripA = DEFAULT_CURRENT_TRIP_A;
  if (!isfinite(cfg.currentSoftA) || cfg.currentSoftA < 0.0f || cfg.currentSoftA > 100.0f) cfg.currentSoftA = DEFAULT_CURRENT_SOFT_A;
  if (!isfinite(cfg.currentFoldPctPerA) || cfg.currentFoldPctPerA < 0.0f || cfg.currentFoldPctPerA > 100.0f) cfg.currentFoldPctPerA = DEFAULT_CURRENT_FOLD_PCT_A;
  if (!isfinite(cfg.currentDroopVPerA) || cfg.currentDroopVPerA < 0.0f || cfg.currentDroopVPerA > 10.0f) cfg.currentDroopVPerA = DEFAULT_CURRENT_DROOP_V_A;
  cfg.currentTripEnable = cfg.currentTripEnable ? 1 : 0;
  cfg.currentFoldbackEnable = cfg.currentFoldbackEnable ? 1 : 0;

  if (!isfinite(cfg.targetV) || cfg.targetV < TARGET_MIN_V || cfg.targetV > TARGET_MAX_V) cfg.targetV = DEFAULT_TARGET_V;
  cfg.kp_x1000 = clampI32(cfg.kp_x1000, 0, 50000);
  cfg.ki_x1000 = clampI32(cfg.ki_x1000, 0, 200000);
  cfg.deadbandMv = clampI32(cfg.deadbandMv, 0, 2000);
  cfg.slewX10PerSec = clampI32(cfg.slewX10PerSec, 1, 20000);
  cfg.integralMinX10 = clampI32(cfg.integralMinX10, -1000, 1000);
  cfg.integralMaxX10 = clampI32(cfg.integralMaxX10, -1000, 1000);
  if (cfg.integralMaxX10 < cfg.integralMinX10) cfg.integralMaxX10 = cfg.integralMinX10;

  cfg.ovpEnable = cfg.ovpEnable ? 1 : 0;
  if (!isfinite(cfg.ovpV) || cfg.ovpV < TARGET_MIN_V || cfg.ovpV > 80.0f) cfg.ovpV = DEFAULT_OVP_V;
  cfg.maxDutyFaultEnable = cfg.maxDutyFaultEnable ? 1 : 0;
  cfg.maxDutyFaultErrMv = clampI32(cfg.maxDutyFaultErrMv, 0, 10000);

  cfg.compRampUpX10PerSec = clampI32(cfg.compRampUpX10PerSec, 1, 20000);
  cfg.compRampDownX10PerSec = clampI32(cfg.compRampDownX10PerSec, 1, 20000);
  cfg.compDacOffsetMv = clampI32(cfg.compDacOffsetMv, -1000, 1000);
  if (cfg.compHystCode > 3) cfg.compHystCode = DEFAULT_COMP_HYST_CODE;

  cfg.autotuneMaxDutyX10 = clampDutyX10(cfg.autotuneMaxDutyX10);
  if (cfg.autotuneMaxDutyX10 > cfg.dutyMaxX10) cfg.autotuneMaxDutyX10 = cfg.dutyMaxX10;
  if (cfg.autotuneMaxDutyX10 < cfg.dutyMinX10 + 50) cfg.autotuneMaxDutyX10 = cfg.dutyMinX10 + 50;
  cfg.autotuneCoarseStepX10 = (uint16_t)clampU32(cfg.autotuneCoarseStepX10, 5, 200);
  cfg.autotuneBinarySteps = (uint8_t)clampU32(cfg.autotuneBinarySteps, 3, 12);
  cfg.autotuneSettleMs = clampU32(cfg.autotuneSettleMs, 20, 3000);
  cfg.autotuneMeasureMs = clampU32(cfg.autotuneMeasureMs, 20, 2000);
  cfg.autotuneTestStepX10 = (uint16_t)clampU32(cfg.autotuneTestStepX10, 5, 100);

  if (!isfinite(cfg.tunedPlantGainVPerPct) || cfg.tunedPlantGainVPerPct < 0.0f || cfg.tunedPlantGainVPerPct > 100.0f) cfg.tunedPlantGainVPerPct = 0.0f;
  if (!isfinite(cfg.tunedPlantTauS) || cfg.tunedPlantTauS < 0.0f || cfg.tunedPlantTauS > 20.0f) cfg.tunedPlantTauS = 0.0f;
  cfg.tunedDutyX10 = clampDutyX10(cfg.tunedDutyX10);
  if (!isfinite(cfg.tunedTargetV) || cfg.tunedTargetV < 0.0f || cfg.tunedTargetV > TARGET_MAX_V) cfg.tunedTargetV = 0.0f;

  if (cfg.activeCalLoadSlot >= CAL_LOAD_SLOT_COUNT) cfg.activeCalLoadSlot = 0;
  for (uint8_t i = 0; i < CAL_LOAD_SLOT_COUNT; i++) {
    if (!isfinite(cfg.calLoadOhms[i]) || cfg.calLoadOhms[i] < 0.0f || cfg.calLoadOhms[i] > 100000.0f) cfg.calLoadOhms[i] = 0.0f;
    cfg.calLoadFreqHz[i] = clampU32(cfg.calLoadFreqHz[i], EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
    cfg.calLoadDutyX10[i] = clampDutyX10(cfg.calLoadDutyX10[i]);
    cfg.calLoadKp_x1000[i] = clampI32(cfg.calLoadKp_x1000[i], 0, 50000);
    cfg.calLoadKi_x1000[i] = clampI32(cfg.calLoadKi_x1000[i], 0, 200000);
    if (!isfinite(cfg.calLoadGainVPerPct[i]) || cfg.calLoadGainVPerPct[i] < 0.0f || cfg.calLoadGainVPerPct[i] > 100.0f) cfg.calLoadGainVPerPct[i] = 0.0f;
    if (!isfinite(cfg.calLoadTauS[i]) || cfg.calLoadTauS[i] < 0.0f || cfg.calLoadTauS[i] > 20.0f) cfg.calLoadTauS[i] = 0.0f;
    if (!isfinite(cfg.calLoadTargetV[i]) || cfg.calLoadTargetV[i] < 0.0f || cfg.calLoadTargetV[i] > TARGET_MAX_V) cfg.calLoadTargetV[i] = 0.0f;
    if (!isfinite(cfg.calLoadMeasuredV[i]) || cfg.calLoadMeasuredV[i] < -5.0f || cfg.calLoadMeasuredV[i] > 100.0f) cfg.calLoadMeasuredV[i] = 0.0f;
    if (!isfinite(cfg.calLoadMeasuredI[i]) || cfg.calLoadMeasuredI[i] < 0.0f || cfg.calLoadMeasuredI[i] > 100.0f) cfg.calLoadMeasuredI[i] = 0.0f;
  }

  controlMode = (ControlMode)cfg.controlMode;
  feedbackPath = (FeedbackPath)cfg.feedbackPath;
  systemEnabled = cfg.systemEnabled ? true : false;
}

// ============================================================
// EEPROM wear leveling
// ============================================================

uint32_t checksumSettings(const SettingsSlot &s) {
  const uint8_t *p = (const uint8_t *)&s;
  uint32_t sum = 0xA5A55A5AUL;
  for (size_t i = 0; i < sizeof(SettingsSlot) - sizeof(uint32_t); i++) {
    sum = (sum << 5) | (sum >> 27);
    sum ^= p[i];
  }
  return sum;
}

void eepromWriteBytes(int addr, const uint8_t *data, size_t len) {
  for (size_t i = 0; i < len; i++) EEPROM.update(addr + i, data[i]);
}

void eepromReadBytes(int addr, uint8_t *data, size_t len) {
  for (size_t i = 0; i < len; i++) data[i] = EEPROM.read(addr + i);
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

void saveSettings() {
  cfg.magic = EEPROM_MAGIC;
  cfg.systemEnabled = systemEnabled ? 1 : 0;
  cfg.controlMode = (uint8_t)controlMode;
  cfg.feedbackPath = (uint8_t)feedbackPath;

  validateSettings();

  cfg.magic = EEPROM_MAGIC;
  cfg.sequence = settingsSequence + 1;
  cfg.systemEnabled = systemEnabled ? 1 : 0;
  cfg.controlMode = (uint8_t)controlMode;
  cfg.feedbackPath = (uint8_t)feedbackPath;
  cfg.checksum = checksumSettings(cfg);

  int nextSlot = (activeSlotIndex + 1) % EEPROM_SLOT_COUNT;
  if (activeSlotIndex < 0) nextSlot = 0;

  eepromWriteBytes(slotAddress(nextSlot), (const uint8_t *)&cfg, sizeof(SettingsSlot));
  settingsSequence = cfg.sequence;
  activeSlotIndex = nextSlot;
}

// ============================================================
// PA10 EN PWM using TIM3 edge-scheduled ISR
// ============================================================

void setPA10High() { GPIOA->BSRR = (1UL << 10); }
void setPA10Low()  { GPIOA->BSRR = (1UL << (10 + 16)); }

uint32_t clampEnFreq(uint32_t hz) {
  return clampU32(hz, cfg.enFreqMinHz, cfg.enFreqMaxHz);
}

uint16_t clampControlDutyLimit(uint16_t dutyX10) {
  if (dutyX10 < cfg.dutyMinX10) dutyX10 = cfg.dutyMinX10;
  if (dutyX10 > cfg.dutyMaxX10) dutyX10 = cfg.dutyMaxX10;
  return dutyX10;
}

void updateEnableTimingNoInterruptLock() {
  uint32_t f = clampEnFreq(enFreqRuntimeHz);
  enFreqRuntimeHz = f;

  uint32_t period = (1000000UL + (f / 2UL)) / f;
  uint32_t minEdge = cfg.enMinEdgeUs;
  if (minEdge < EN_MIN_EDGE_HARD_US) minEdge = EN_MIN_EDGE_HARD_US;
  if (minEdge > EN_MAX_EDGE_HARD_US) minEdge = EN_MAX_EDGE_HARD_US;
  if (period < 2UL * minEdge) period = 2UL * minEdge;

  uint16_t rawCmd = enDutyCmdX10;
  uint16_t cmd = rawCmd;
  if (rawCmd != 0) {
    cmd = clampControlDutyLimit(cmd);
  }

  uint32_t high = ((uint64_t)period * (uint64_t)cmd + 500ULL) / 1000ULL;

  if (rawCmd == 0 || cmd == 0) {
    high = 0;
  } else if (cmd >= 1000 && cfg.allowStatic100) {
    high = period;
  } else {
    if (high < minEdge) high = minEdge;
    if (high > period - minEdge) high = period - minEdge;
  }

  enPeriodUs = period;
  enHighUs = high;
  if (period == 0) enDutyEffX10 = 0;
  else enDutyEffX10 = (uint16_t)((1000UL * high + period / 2UL) / period);
}

uint32_t enCompareUsForTimer() {
  uint32_t period = enPeriodUs;
  uint32_t high = enHighUs;
  if (period < 2UL) period = 2UL;
  if (high == 0 || high >= period) return period - 1UL;
  return high;
}

void applyEnableTimerPeriodNoInterruptLock() {
  if (EnTimer == nullptr) return;

  uint32_t period = enPeriodUs;
  if (period < 2UL) period = 2UL;
  uint32_t cmp = enCompareUsForTimer();

  EnTimer->setOverflow(period, MICROSEC_FORMAT);
  EnTimer->setCaptureCompare(1, cmp, MICROSEC_COMPARE_FORMAT);
  enTimerAppliedPeriodUs = period;
  enTimerAppliedHighUs = enHighUs;
}

void applyEnableTimerCompareNoInterruptLock() {
  if (EnTimer == nullptr) return;

  uint32_t high = enHighUs;
  if (high == enTimerAppliedHighUs) return;
  EnTimer->setCaptureCompare(1, enCompareUsForTimer(), MICROSEC_COMPARE_FORMAT);
  enTimerAppliedHighUs = high;
}

void enPeriodISR() {
  uint32_t period = enPeriodUs;
  uint32_t high = enHighUs;

  if (!systemEnabled || faultLatched || high == 0 || enDutyEffX10 == 0) {
    setPA10Low();
    enPwmStateHigh = false;
    return;
  }

  setPA10High();
  enPwmStateHigh = true;
}

void enCompareISR() {
  uint32_t period = enPeriodUs;
  uint32_t high = enHighUs;

  if (!systemEnabled || faultLatched || high == 0 || enDutyEffX10 == 0) {
    setPA10Low();
    enPwmStateHigh = false;
    return;
  }

  if (!enPwmStateHigh) return;
  if (high >= period) return;

  setPA10Low();
  enPwmStateHigh = false;
}

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
  enTimerAppliedPeriodUs = enPeriodUs;
  enTimerAppliedHighUs = enHighUs;
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
  applyEnableTimerPeriodNoInterruptLock();
  interrupts();
}

void setEnDutyX10(uint16_t dutyX10) {
  noInterrupts();
  enDutyCmdX10 = clampDutyX10(dutyX10);
  updateEnableTimingNoInterruptLock();
  applyEnableTimerCompareNoInterruptLock();
  if (enHighUs == 0 || !systemEnabled || faultLatched) {
    setPA10Low();
    enPwmStateHigh = false;
  } else if (enHighUs >= enPeriodUs) {
    setPA10High();
    enPwmStateHigh = true;
  }
  interrupts();
}

float getCmdDutyPercent() { return dutyX10ToPercent(enDutyCmdX10); }
float getEffDutyPercent() { return dutyX10ToPercent(enDutyEffX10); }

// ============================================================
// Fixed TIM1 PA8 / PA9 gate drive
// ============================================================

void setupPA8PA9_TIM1_AF2() {
#if defined(RCC_IOPENR_GPIOAEN)
  RCC->IOPENR |= RCC_IOPENR_GPIOAEN;
#endif

  GPIOA->MODER &= ~(0b11UL << (8 * 2));
  GPIOA->MODER |=  (0b10UL << (8 * 2));
  GPIOA->MODER &= ~(0b11UL << (9 * 2));
  GPIOA->MODER |=  (0b10UL << (9 * 2));

  GPIOA->OTYPER &= ~(1UL << 8);
  GPIOA->OTYPER &= ~(1UL << 9);

  GPIOA->OSPEEDR &= ~(0b11UL << (8 * 2));
  GPIOA->OSPEEDR |=  (0b11UL << (8 * 2));
  GPIOA->OSPEEDR &= ~(0b11UL << (9 * 2));
  GPIOA->OSPEEDR |=  (0b11UL << (9 * 2));

  GPIOA->PUPDR &= ~(0b11UL << (8 * 2));
  GPIOA->PUPDR &= ~(0b11UL << (9 * 2));

  GPIOA->AFR[1] &= ~(0xFUL << ((8 - 8) * 4));
  GPIOA->AFR[1] |=  (0x2UL << ((8 - 8) * 4));
  GPIOA->AFR[1] &= ~(0xFUL << ((9 - 8) * 4));
  GPIOA->AFR[1] |=  (0x2UL << ((9 - 8) * 4));
}

bool calculateGateTiming(uint32_t &arr, uint32_t &ccr1, uint32_t &ccr2, uint32_t &deadTicks, uint32_t &actualDeadNs) {
  uint32_t timClk = getTimerClockHz();
  arr = (timClk / (2UL * GATE_FREQ_HZ)) - 1UL;
  if (arr < 8) return false;

  deadTicks = (uint32_t)(((uint64_t)GATE_DEADTIME_NS * (uint64_t)timClk + 500000000ULL) / 1000000000ULL);
  if (GATE_DEADTIME_NS > 0 && deadTicks < 1) deadTicks = 1;

  uint32_t half = (arr + 1UL) / 2UL;
  uint32_t leftTicks = deadTicks / 2UL;
  uint32_t rightTicks = deadTicks - leftTicks;

  if (leftTicks >= half) leftTicks = half - 1UL;

  uint32_t maxRightTicks = (arr > half) ? (arr - half) : 0UL;
  if (rightTicks > maxRightTicks) rightTicks = maxRightTicks;

  ccr1 = half - leftTicks;
  ccr2 = half + rightTicks;
  if (ccr1 < 1) ccr1 = 1;
  if (ccr2 > arr) ccr2 = arr;

  if (GATE_DEADTIME_NS > 0 && ccr2 <= ccr1) return false;

  deadTicks = (ccr2 > ccr1) ? (ccr2 - ccr1) : 0UL;
  actualDeadNs = (uint32_t)(((uint64_t)deadTicks * 1000000000ULL) / (uint64_t)timClk);
  return true;
}

void applyGateSettingsFixed() {
  uint32_t arr, ccr1, ccr2, deadTicks, actualDeadNs;
  if (!calculateGateTiming(arr, ccr1, ccr2, deadTicks, actualDeadNs)) {
    CmdSerial.println("ERROR: TIM1 fixed gate timing invalid for current clock.");
    return;
  }

  noInterrupts();
  TIM1->ARR = arr;
  TIM1->CCR1 = ccr1;
  TIM1->CCR2 = ccr2;
  TIM1->EGR = 1;
  interrupts();

  CmdSerial.print("TIM1 fixed PA8/PA9: ");
  CmdSerial.print(GATE_FREQ_HZ);
  CmdSerial.print(" Hz, requested DT ");
  CmdSerial.print(GATE_DEADTIME_NS);
  CmdSerial.print(" ns, actual approx ");
  CmdSerial.print(actualDeadNs);
  CmdSerial.println(" ns");
}

void setGateOutputsEnabled(bool enable) {
#if KEEP_GATE_PWM_RUNNING
  (void)enable;
  TIM1->BDTR |= (1UL << 15); // MOE
  TIM1->CR1 |= 1UL;          // CEN

  if (!enable) {
    setPA10Low();
    enPwmStateHigh = false;
  }
#else
  if (enable) {
    TIM1->BDTR |= (1UL << 15); // MOE
    TIM1->CR1 |= 1UL;          // CEN
  } else {
    TIM1->BDTR &= ~(1UL << 15);
    setPA10Low();
    enPwmStateHigh = false;
  }
#endif
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
  TIM1->CCER |= (1UL << 0);    // CH1 enable
  TIM1->CCER |= (1UL << 4);    // CH2 enable

  TIM1->BDTR = 0;
  TIM1->CR1 = 0;
  TIM1->CR1 |= (1UL << 5);     // center-aligned mode 1
  TIM1->CR1 |= (1UL << 7);     // ARR preload

  applyGateSettingsFixed();
  setGateOutputsEnabled(systemEnabled && !faultLatched);

#if KEEP_GATE_PWM_RUNNING
  CmdSerial.println("TIM1 PA8/PA9 carrier is kept running; PA10 EN is the shutdown actuator.");
#endif
}

// ============================================================
// ADC scaling and sensor readback
// ============================================================

float dividerRatio() {
  return cfg.vdivBottomK / (cfg.vdivTopK + cfg.vdivBottomK);
}

float adcCountsToVoltage(uint16_t counts) {
  return ((float)counts * cfg.adcRefV) / (float)ADC_MAX_COUNTS;
}

uint16_t readAdcAveragedFast(uint8_t pin, uint16_t samples) {
  for (uint16_t i = 0; i < cfg.adcDummy; i++) (void)analogRead(pin);
  uint32_t sum = 0;
  for (uint16_t i = 0; i < samples; i++) sum += analogRead(pin);
  return (uint16_t)(sum / samples);
}

float amcOutputToInputVoltage(float amcOutV) {
  return ((amcOutV - (cfg.amcRefV * 0.5f)) * 2.0f * cfg.amcVclipV) / cfg.amcRefV;
}

float amcInputToSecondaryVoltage(float amcInputV) {
  float ratio = dividerRatio();
  if (ratio <= 0.0f) ratio = 1.0f / 40.0f;
  return ((amcInputV / ratio) * cfg.voutGain) + cfg.voutOffsetV;
}

float secondaryVoltageToPa1Voltage(float secondaryV) {
  float ratio = dividerRatio();
  float amcInput = secondaryV * ratio;
  return (cfg.amcRefV * 0.5f) + (amcInput * cfg.amcRefV) / (2.0f * cfg.amcVclipV);
}

float readSecondaryVoltageRaw(bool *validOut, bool *satOut) {
  bool valid = true;
  bool sat = false;

  rawPa1Adc = readAdcAveragedFast(SENSE_VOUT_PIN, cfg.adcVSamples);
  rawPa1Voltage = adcCountsToVoltage(rawPa1Adc);

  if (rawPa1Voltage < cfg.sensorMinPa1V) valid = false;
  if (rawPa1Voltage > cfg.adcRefV - 0.050f) sat = true;

  float amcInput = amcOutputToInputVoltage(rawPa1Voltage);
  float vout = amcInputToSecondaryVoltage(amcInput);
  if (vout < 0.0f && vout > -0.75f) vout = 0.0f;

  if (!valid && filtersPrimed) vout = filteredVout;

  if (validOut) *validOut = valid;
  if (satOut) *satOut = sat;
  return vout;
}

float readHBridgeCurrentRaw() {
  if (!currentSenseAvailable()) {
    rawPa2Adc = 0;
    rawPa2Voltage = 0.0f;
    return 0.0f;
  }

  rawPa2Adc = readAdcAveragedFast(SENSE_CURRENT_PIN, cfg.adcISamples);
  rawPa2Voltage = adcCountsToVoltage(rawPa2Adc);

  float denom = cfg.csResOhms * cfg.csGainAperA;
  if (denom <= 0.000001f) denom = DEFAULT_CS_RES_OHMS * DEFAULT_CS_GAIN_A_PER_A;

  float amps = (rawPa2Voltage - cfg.currentOffsetV) / denom;
  if (amps < 0.0f) amps = 0.0f;
  return amps;
}

void updateAnalogFilters(bool readVoltage, bool readCurrent) {
  uint32_t blockStartUs = micros();
  bool valid = latestSensorValid;
  bool sat = latestSensorSaturated;
  float v = latestVoutRaw;
  float i = latestCurrentRaw;

  if (readVoltage) v = readSecondaryVoltageRaw(&valid, &sat);
  readCurrent = readCurrent && currentSenseAvailable();
  if (readCurrent) i = readHBridgeCurrentRaw();

  uint32_t blockUs = micros() - blockStartUs;
  lastAdcBlockUs = blockUs;
  if (blockUs > maxAdcBlockUs) maxAdcBlockUs = blockUs;

  uint32_t nowUs = micros();
  float dt = 0.001f;
  if (lastAnalogUs != 0) {
    dt = ((float)(nowUs - lastAnalogUs)) / 1000000.0f;
    dt = clampFloat(dt, 0.00005f, 0.5f);
  }
  lastAnalogUs = nowUs;

  latestVoutRaw = v;
  latestCurrentRaw = i;
  latestSensorValid = valid;
  latestSensorSaturated = sat;

  if (!filtersPrimed) {
    filteredVout = v;
    filteredCurrent = i;
    filtersPrimed = true;
    return;
  }

  if (readVoltage && valid) {
    float tau = cfg.voutTauMs / 1000.0f;
    float a = dt / (tau + dt);
    a = clampFloat(a, 0.001f, 1.0f);
    filteredVout += a * (v - filteredVout);
  }

  if (readCurrent) {
    float tau = cfg.currentTauMs / 1000.0f;
    float a = dt / (tau + dt);
    a = clampFloat(a, 0.001f, 1.0f);
    filteredCurrent += a * (i - filteredCurrent);
  }
}

// ============================================================
// Comparator path: COMP1 plus = PA1 IO3, minus = DAC1_CH1
// ============================================================

#ifndef COMP_CSR_EN
#define COMP_CSR_EN (1UL << 0)
#endif
#ifndef COMP_CSR_INMSEL_0
#define COMP_CSR_INMSEL_0 (1UL << 4)
#define COMP_CSR_INMSEL_1 (1UL << 5)
#define COMP_CSR_INMSEL_2 (1UL << 6)
#define COMP_CSR_INMSEL_3 (1UL << 7)
#endif
#ifndef COMP_CSR_INPSEL_0
#define COMP_CSR_INPSEL_0 (1UL << 8)
#define COMP_CSR_INPSEL_1 (1UL << 9)
#endif
#ifndef COMP_CSR_HYST_0
#define COMP_CSR_HYST_0 (1UL << 16)
#define COMP_CSR_HYST_1 (1UL << 17)
#endif
#ifndef COMP_CSR_VALUE
#define COMP_CSR_VALUE (1UL << 30)
#endif

uint32_t compHystBits() {
  switch (cfg.compHystCode) {
    case 1: return COMP_CSR_HYST_0;
    case 2: return COMP_CSR_HYST_1;
    case 3: return COMP_CSR_HYST_1 | COMP_CSR_HYST_0;
    default: return 0;
  }
}

void updateComparatorDacThreshold() {
  float thresholdV = secondaryVoltageToPa1Voltage(cfg.targetV);
  thresholdV += ((float)cfg.compDacOffsetMv) / 1000.0f;
  thresholdV = clampFloat(thresholdV, 0.0f, cfg.adcRefV);
  uint16_t newCode = (uint16_t)((thresholdV / cfg.adcRefV) * 4095.0f + 0.5f);
  if (newCode > 4095) newCode = 4095;

  if (compDacWritten && newCode == compDacCode) return;
  compDacCode = newCode;
  compDacWritten = true;

#if defined(RCC_APBENR1_DAC1EN)
  RCC->APBENR1 |= RCC_APBENR1_DAC1EN;
#endif
#if defined(DAC1) && defined(DAC_CR_EN1)
  DAC1->DHR12R1 = compDacCode;
  DAC1->CR |= DAC_CR_EN1;
#else
  analogWriteResolution(12);
  analogWrite(COMP_DAC_PIN, compDacCode);
#endif
}

void setupComparatorHardware() {
  updateComparatorDacThreshold();

#if defined(RCC_APBENR2_SYSCFGEN)
  RCC->APBENR2 |= RCC_APBENR2_SYSCFGEN;
#elif defined(RCC_APB2ENR_SYSCFGEN)
  RCC->APB2ENR |= RCC_APB2ENR_SYSCFGEN;
#endif

#if defined(COMP1)
  pinMode(SENSE_VOUT_PIN, INPUT_ANALOG);
  uint32_t csr = 0;
  // COMP1 input plus IO3 = PA1. Minus DAC1_CH1 = COMP_CSR_INMSEL_2.
  csr |= COMP_CSR_INPSEL_1;
  csr |= COMP_CSR_INMSEL_2;
  csr |= compHystBits();
  COMP1->CSR = csr;
  COMP1->CSR = csr | COMP_CSR_EN;
  delayMicroseconds(20);
  comparatorConfigured = true;
#else
  comparatorConfigured = false;
#endif
}

bool comparatorAboveTarget() {
  if (!comparatorConfigured) setupComparatorHardware();
#if defined(COMP1)
  compLastAbove = (COMP1->CSR & COMP_CSR_VALUE) ? true : false;
#else
  compLastAbove = latestVoutRaw >= cfg.targetV;
#endif
  return compLastAbove;
}

// ============================================================
// Fault handling
// ============================================================

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

bool checkFaults(bool haveVoltage, bool haveCurrent) {
  if (faultLatched) return true;

  haveCurrent = haveCurrent && currentSenseAvailable();

  if (haveCurrent && cfg.currentTripEnable && filteredCurrent > cfg.currentTripA) {
    latchFault(FAULT_CURRENT, "primary current trip");
    return true;
  }

  if (haveVoltage && cfg.ovpEnable && latestSensorValid && filteredVout > cfg.ovpV) {
    latchFault(FAULT_OVP, "output over-voltage");
    return true;
  }

  return false;
}

// ============================================================
// Mode control
// ============================================================

void startSensorPowerup(uint16_t requestedDutyX10) {
  sensorPowerupActive = true;
  sensorPowerupStartMs = millis();
  sensorPowerupDutyActiveX10 = clampDutyX10(requestedDutyX10);
  if (sensorPowerupDutyActiveX10 < cfg.powerupDutyX10) sensorPowerupDutyActiveX10 = cfg.powerupDutyX10;
  if (sensorPowerupDutyActiveX10 > cfg.dutyMaxX10) sensorPowerupDutyActiveX10 = cfg.dutyMaxX10;

  controlDutyPercent = dutyX10ToPercent(sensorPowerupDutyActiveX10);
  comparatorDutyX10 = (float)sensorPowerupDutyActiveX10;
  closedLoopIntegratorPct = 0.0f;
  filtersPrimed = false;
  setEnDutyX10(sensorPowerupDutyActiveX10);
}

bool handleSensorPowerup() {
  if (!sensorPowerupActive) return false;
  setEnDutyX10(sensorPowerupDutyActiveX10);
  bool needCurrentAdc = currentProtectionEnabled() || feedbackUsesCurrent();
  updateAnalogFilters(true, needCurrentAdc);
  checkFaults(true, needCurrentAdc);

  if (millis() - sensorPowerupStartMs >= 750UL) {
    sensorPowerupActive = false;
    filtersPrimed = false;
    closedLoopIntegratorPct = 0.0f;

    uint16_t seed = cfg.biasDutyX10;
    if (cfg.tunedTargetV == cfg.targetV && cfg.tunedDutyX10 > 0) seed = cfg.tunedDutyX10;
    seed = clampControlDutyLimit(seed);
    controlDutyPercent = dutyX10ToPercent(seed);
    comparatorDutyX10 = (float)seed;
    setEnDutyX10(seed);
    return false;
  }
  return true;
}

void applyModeState(bool save) {
  updateModeLEDs();

  if (!systemEnabled || faultLatched) {
    sensorPowerupActive = false;
    setEnDutyX10(0);
    setGateOutputsEnabled(false);
  } else {
    setGateOutputsEnabled(true);
    setEnFrequencyHz(cfg.enFreqHz);

    if (feedbackUsesComparator()) setupComparatorHardware();

    if (controlMode == MODE_OPEN_LOOP) {
      sensorPowerupActive = false;
      controlDutyPercent = dutyX10ToPercent(cfg.openLoopDutyX10);
      comparatorDutyX10 = (float)cfg.openLoopDutyX10;
      setEnDutyX10(cfg.openLoopDutyX10);
    } else {
      uint16_t seed = cfg.biasDutyX10;
      if (cfg.tunedTargetV == cfg.targetV && cfg.tunedDutyX10 > 0) seed = cfg.tunedDutyX10;
      startSensorPowerup(seed);
    }
  }

  if (save) saveSettings();
}

void setMode(ControlMode mode, bool save) {
  controlMode = mode;
  cfg.controlMode = (uint8_t)mode;
  faultLatched = false;
  faultCode = FAULT_NONE;
  closedLoopIntegratorPct = 0.0f;
  maxDutyStartMs = 0;
  applyModeState(save);
}

void setSystemEnabled(bool enable, bool save) {
  systemEnabled = enable;
  cfg.systemEnabled = enable ? 1 : 0;
  faultLatched = false;
  faultCode = FAULT_NONE;
  closedLoopIntegratorPct = 0.0f;
  maxDutyStartMs = 0;
  applyModeState(save);
}

void setFeedbackPath(FeedbackPath p, bool save) {
  feedbackPath = p;
  cfg.feedbackPath = (uint8_t)p;
  closedLoopIntegratorPct = 0.0f;
  comparatorConfigured = false;
  if (feedbackUsesComparator()) setupComparatorHardware();
  applyModeState(save);
}

// ============================================================
// Current helper
// ============================================================

float currentFoldbackTrimPercent() {
  if (!feedbackUsesCurrent()) return 0.0f;
  if (!cfg.currentFoldbackEnable) return 0.0f;
  if (filteredCurrent <= cfg.currentSoftA) return 0.0f;
  return -cfg.currentFoldPctPerA * (filteredCurrent - cfg.currentSoftA);
}

float effectiveTargetVoltage() {
  float t = cfg.targetV;
  if (feedbackUsesCurrent() && cfg.currentDroopVPerA > 0.0f) {
    t -= cfg.currentDroopVPerA * filteredCurrent;
    if (t < TARGET_MIN_V) t = TARGET_MIN_V;
  }
  return t;
}

// ============================================================
// Closed-loop control
// ============================================================

void handleMaxDutyProtection(float errorV) {
  bool atMax = ((uint16_t)dutyPercentToX10(controlDutyPercent)) >= (cfg.dutyMaxX10 - 1);
  bool pushing = errorV > ((float)cfg.maxDutyFaultErrMv / 1000.0f);

  if (atMax && pushing) {
    if (maxDutyStartMs == 0) maxDutyStartMs = millis();
    if (cfg.maxDutyFaultEnable && millis() - maxDutyStartMs >= cfg.maxDutyFaultMs) {
      latchFault(FAULT_MAX_DUTY, "closed loop at max EN duty and still below target");
    }
  } else {
    maxDutyStartMs = 0;
  }
}

void handleVoltagePid(float dt) {
  float targetV = effectiveTargetVoltage();
  float errorV = targetV - filteredVout;
  if (fabsf(errorV) < ((float)cfg.deadbandMv / 1000.0f)) errorV = 0.0f;

  float kp = ((float)cfg.kp_x1000) / 1000.0f;
  float ki = ((float)cfg.ki_x1000) / 1000.0f;
  float bias = dutyX10ToPercent(cfg.biasDutyX10);
  float fold = currentFoldbackTrimPercent();

  float pTerm = kp * errorV;
  float preSat = bias + pTerm + closedLoopIntegratorPct + fold;
  float dutyMinPct = dutyX10ToPercent(cfg.dutyMinX10);
  float dutyMaxPct = dutyX10ToPercent(cfg.dutyMaxX10);

  bool highSatPush = (preSat >= dutyMaxPct && errorV > 0.0f);
  bool lowSatPush = (preSat <= dutyMinPct && errorV < 0.0f);
  bool foldbackActive = fold < -0.001f && errorV > 0.0f;

  if (!highSatPush && !lowSatPush && !foldbackActive) {
    closedLoopIntegratorPct += ki * errorV * dt;
    closedLoopIntegratorPct = clampFloat(
      closedLoopIntegratorPct,
      ((float)cfg.integralMinX10) / 10.0f,
      ((float)cfg.integralMaxX10) / 10.0f
    );
  }

  float requested = bias + pTerm + closedLoopIntegratorPct + fold;
  requested = clampFloat(requested, dutyMinPct, dutyMaxPct);

  float maxStepPct = (((float)cfg.slewX10PerSec) / 10.0f) * dt;
  if (maxStepPct < 0.01f) maxStepPct = 0.01f;
  if (maxStepPct > 10.0f) maxStepPct = 10.0f;

  float delta = requested - controlDutyPercent;
  delta = clampFloat(delta, -maxStepPct, maxStepPct);
  controlDutyPercent += delta;
  controlDutyPercent = clampFloat(controlDutyPercent, dutyMinPct, dutyMaxPct);

  setEnDutyX10(dutyPercentToX10(controlDutyPercent));
  handleMaxDutyProtection(errorV);
}

void handleComparatorControl(float dt) {
  updateComparatorDacThreshold();
  bool above = comparatorAboveTarget();

  float stepUp = ((float)cfg.compRampUpX10PerSec) * dt;
  float stepDn = ((float)cfg.compRampDownX10PerSec) * dt;
  if (stepUp < 0.05f) stepUp = 0.05f;
  if (stepDn < 0.05f) stepDn = 0.05f;

  if (above) comparatorDutyX10 -= stepDn;
  else comparatorDutyX10 += stepUp;

  if (feedbackUsesCurrent() && cfg.currentFoldbackEnable && filteredCurrent > cfg.currentSoftA) {
    float overA = filteredCurrent - cfg.currentSoftA;
    comparatorDutyX10 -= (cfg.currentFoldPctPerA * 10.0f) * overA * dt;
  }

  comparatorDutyX10 = clampFloat(comparatorDutyX10, (float)cfg.dutyMinX10, (float)cfg.dutyMaxX10);
  controlDutyPercent = comparatorDutyX10 * 0.1f;
  setEnDutyX10((uint16_t)(comparatorDutyX10 + 0.5f));

  // For comparator mode, this is only a protection/status check. The actual voltage decision is COMP1.
  float err = cfg.targetV - filteredVout;
  handleMaxDutyProtection(err);
}

void handleClosedLoopControl() {
  static uint32_t lastControlUs = 0;

  if (!systemEnabled || controlMode != MODE_CLOSED_LOOP) return;
  if (faultLatched) {
    setEnDutyX10(0);
    return;
  }

  if (handleSensorPowerup()) return;

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
  dt = clampFloat(dt, 0.00005f, 0.1f);

  bool needVoltageAdc = feedbackUsesVoltagePid() || cfg.ovpEnable || !feedbackUsesComparator();
  bool needCurrentAdc = currentProtectionEnabled() || feedbackUsesCurrent();
  updateAnalogFilters(needVoltageAdc, needCurrentAdc);

  if (checkFaults(needVoltageAdc, needCurrentAdc)) return;

  if (feedbackUsesVoltagePid() && !latestSensorValid) {
    setEnDutyX10(cfg.powerupDutyX10);
    controlDutyPercent = dutyX10ToPercent(cfg.powerupDutyX10);
    closedLoopIntegratorPct = 0.0f;
    return;
  }

  if (feedbackUsesVoltagePid()) handleVoltagePid(dt);
  else handleComparatorControl(dt);
}

// ============================================================
// Autotune
// ============================================================

void initMeasure(MeasureResult &m) {
  m.avgV = 0.0f;
  m.minV = 99999.0f;
  m.maxV = -99999.0f;
  m.avgI = 0.0f;
  m.avgPa1 = 0.0f;
  m.avgPa2 = 0.0f;
  m.avgAdc1 = 0;
  m.avgAdc2 = 0;
  m.count = 0;
  m.avgBlockUs = 0;
  m.valid = false;
  m.sat = false;
  m.fault = false;
}

bool serviceDelayMs(uint32_t ms) {
  uint32_t start = millis();
  while (millis() - start < ms) {
    handleClosedLoopControl();
    bool needCurrentAdc = currentSenseAvailable();
    updateAnalogFilters(true, needCurrentAdc);
    if (checkFaults(true, needCurrentAdc)) return false;
    delay(1);
  }
  return true;
}

MeasureResult measureWindow(uint32_t ms) {
  MeasureResult m;
  initMeasure(m);
  uint32_t sumAdc1 = 0;
  uint32_t sumAdc2 = 0;
  uint32_t sumBlock = 0;
  uint32_t start = millis();

  while (millis() - start < ms) {
    bool needCurrentAdc = currentSenseAvailable();
    updateAnalogFilters(true, needCurrentAdc);
    if (checkFaults(true, needCurrentAdc)) {
      m.fault = true;
      break;
    }

    if (latestSensorValid) {
      m.avgV += latestVoutRaw;
      if (latestVoutRaw < m.minV) m.minV = latestVoutRaw;
      if (latestVoutRaw > m.maxV) m.maxV = latestVoutRaw;
      m.valid = true;
    }
    if (latestSensorSaturated) m.sat = true;
    m.avgI += latestCurrentRaw;
    m.avgPa1 += rawPa1Voltage;
    m.avgPa2 += rawPa2Voltage;
    sumAdc1 += rawPa1Adc;
    sumAdc2 += rawPa2Adc;
    sumBlock += lastAdcBlockUs;
    m.count++;
    delay(2);
  }

  if (m.count == 0) m.count = 1;
  if (m.valid) m.avgV /= (float)m.count;
  else {
    m.avgV = filteredVout;
    m.minV = filteredVout;
    m.maxV = filteredVout;
  }
  m.avgI /= (float)m.count;
  m.avgPa1 /= (float)m.count;
  m.avgPa2 /= (float)m.count;
  m.avgAdc1 = (uint16_t)(sumAdc1 / m.count);
  m.avgAdc2 = (uint16_t)(sumAdc2 / m.count);
  m.avgBlockUs = sumBlock / m.count;
  return m;
}

MeasureResult settleAndMeasure(uint32_t settleMs, uint32_t measureMs) {
  serviceDelayMs(settleMs);
  return measureWindow(measureMs);
}

void printMeasure(const char *tag, uint16_t dutyX10, const MeasureResult &m) {
  CmdSerial.print(tag);
  CmdSerial.print(" FEN="); CmdSerial.print(enFreqRuntimeHz);
  CmdSerial.print("Hz Dcmd="); CmdSerial.print(dutyX10ToPercent(dutyX10), 1);
  CmdSerial.print("% Deff="); CmdSerial.print(getEffDutyPercent(), 1);
  CmdSerial.print("% V="); CmdSerial.print(m.avgV, 3);
  CmdSerial.print(" min="); CmdSerial.print(m.minV, 3);
  CmdSerial.print(" max="); CmdSerial.print(m.maxV, 3);
  CmdSerial.print(" I="); CmdSerial.print(m.avgI, 3);
  CmdSerial.print(" PA1="); CmdSerial.print(m.avgAdc1);
  CmdSerial.print("/"); CmdSerial.print(m.avgPa1, 4);
  CmdSerial.print("V ADCus="); CmdSerial.print(m.avgBlockUs);
  if (!m.valid) CmdSerial.print(" SENSOR_INVALID");
  if (m.sat) CmdSerial.print(" SENSOR_SAT");
  if (m.fault) CmdSerial.print(" FAULT");
  CmdSerial.println();
}

bool autotunePowerSensor(float targetV) {
  CmdSerial.println("AUTOTUNE: sensor power-up");
  uint16_t start = cfg.powerupDutyX10;
  if (start < 10) start = 10;
  uint16_t maxD = cfg.autotuneMaxDutyX10;
  if (maxD > cfg.dutyMaxX10) maxD = cfg.dutyMaxX10;

  for (uint16_t d = start; d <= maxD; d += 20) {
    setEnDutyX10(d);
    filtersPrimed = false;
    MeasureResult m = settleAndMeasure(120, 80);
    printMeasure("PWR", d, m);
    if (m.fault) return false;
    if (m.valid && m.avgPa1 >= cfg.sensorMinPa1V) {
      cfg.powerupDutyX10 = d;
      return true;
    }
    if (m.valid && m.avgV > targetV + 1.0f) return false;
  }
  return false;
}

bool autotuneFindDuty(float targetV, uint16_t &bestDutyX10, float &bestV, float &bestErr, float &bestRipple) {
  CmdSerial.println("AUTOTUNE: duty search without touching PA8/PA9");
  bestDutyX10 = cfg.dutyMinX10;
  bestV = 0.0f;
  bestErr = 99999.0f;
  bestRipple = 99999.0f;
  bool have = false;

  uint16_t lo = cfg.dutyMinX10;
  uint16_t hi = cfg.autotuneMaxDutyX10;
  if (hi > cfg.dutyMaxX10) hi = cfg.dutyMaxX10;

  uint16_t lastBelow = lo;
  uint16_t firstAbove = hi;
  bool bracketed = false;

  for (uint16_t d = lo; d <= hi; d = (uint16_t)(d + cfg.autotuneCoarseStepX10)) {
    setEnDutyX10(d);
    filtersPrimed = false;
    MeasureResult m = settleAndMeasure(cfg.autotuneSettleMs, cfg.autotuneMeasureMs);
    printMeasure("COARSE", d, m);
    if (m.fault) return false;
    if (!m.valid) continue;

    float err = fabsf(targetV - m.avgV);
    if (err < bestErr) {
      bestErr = err;
      bestV = m.avgV;
      bestDutyX10 = d;
      bestRipple = m.maxV - m.minV;
      have = true;
    }

    if (m.avgV < targetV) {
      lastBelow = d;
    } else {
      firstAbove = d;
      bracketed = true;
      break;
    }

    if (hi - d < cfg.autotuneCoarseStepX10) break;
  }

  if (!have) return false;
  if (!bracketed) return true;

  CmdSerial.println("AUTOTUNE: binary trim");
  uint16_t a = lastBelow;
  uint16_t b = firstAbove;
  for (uint8_t k = 0; k < cfg.autotuneBinarySteps; k++) {
    uint16_t mid = (uint16_t)((a + b) / 2U);
    setEnDutyX10(mid);
    filtersPrimed = false;
    MeasureResult m = settleAndMeasure(cfg.autotuneSettleMs, cfg.autotuneMeasureMs);
    printMeasure("BIN", mid, m);
    if (m.fault) return false;
    if (!m.valid) continue;

    float err = fabsf(targetV - m.avgV);
    if (err < bestErr) {
      bestErr = err;
      bestV = m.avgV;
      bestDutyX10 = mid;
      bestRipple = m.maxV - m.minV;
    }

    if (m.avgV < targetV) a = mid;
    else b = mid;
  }
  return true;
}

float autotuneLoadPenalty(float targetV, const MeasureResult &m, int8_t loadSlot) {
  if (loadSlot < 0 || !validLoadSlot((uint8_t)loadSlot)) return 0.0f;
  float expectedI = expectedLoadCurrentA((uint8_t)loadSlot);
  if (expectedI <= 0.01f || !currentSenseAvailable()) return 0.0f;
  if (m.avgI <= 0.001f) return 0.0f;

  float relErr = fabsf(m.avgI - expectedI) / expectedI;
  relErr = clampFloat(relErr, 0.0f, 3.0f);
  return relErr * 0.05f * targetV;
}

float autotuneScorePoint(float targetV, uint16_t dutyX10, const MeasureResult &m, int8_t loadSlot) {
  float err = fabsf(targetV - m.avgV);
  float ripple = m.maxV - m.minV;
  if (ripple < 0.0f || !isfinite(ripple)) ripple = 0.0f;
  float dutyPenalty = dutyX10ToPercent(dutyX10) * 0.002f;
  float score = err + (0.20f * ripple) + dutyPenalty + autotuneLoadPenalty(targetV, m, loadSlot);
  if (m.sat) score += 5.0f;
  return score;
}

bool considerFullTunePoint(const char *tag, uint16_t dutyX10, float targetV,
                           const MeasureResult &m, int8_t loadSlot,
                           uint16_t &bestDutyX10, float &bestV,
                           float &bestErr, float &bestRipple,
                           float &bestScore, bool &haveBest) {
  printMeasure(tag, dutyX10, m);
  if (m.fault) return false;
  if (!m.valid) return true;

  float err = fabsf(targetV - m.avgV);
  float ripple = m.maxV - m.minV;
  if (ripple < 0.0f || !isfinite(ripple)) ripple = 0.0f;
  float score = autotuneScorePoint(targetV, dutyX10, m, loadSlot);

  if (!haveBest || score < bestScore) {
    haveBest = true;
    bestScore = score;
    bestDutyX10 = dutyX10;
    bestV = m.avgV;
    bestErr = err;
    bestRipple = ripple;
  }
  return true;
}

bool autotuneFindDutyFull(float targetV, int8_t loadSlot, uint16_t &bestDutyX10,
                          float &bestV, float &bestErr, float &bestRipple,
                          float &bestScore) {
  CmdSerial.println("AUTOTUNE FULL: exhaustive duty scan; no monotonic assumption");
  bestDutyX10 = cfg.dutyMinX10;
  bestV = 0.0f;
  bestErr = 99999.0f;
  bestRipple = 99999.0f;
  bestScore = 999999.0f;
  bool haveBest = false;

  uint16_t lo = cfg.dutyMinX10;
  uint16_t hi = cfg.autotuneMaxDutyX10;
  if (hi > cfg.dutyMaxX10) hi = cfg.dutyMaxX10;
  uint16_t coarseStep = cfg.autotuneCoarseStepX10;
  if (coarseStep < 5) coarseStep = 5;

  for (uint16_t d = lo; d <= hi; ) {
    setEnDutyX10(d);
    filtersPrimed = false;
    MeasureResult m = settleAndMeasure(cfg.autotuneSettleMs, cfg.autotuneMeasureMs);
    if (!considerFullTunePoint("FULL", d, targetV, m, loadSlot, bestDutyX10, bestV,
                               bestErr, bestRipple, bestScore, haveBest)) {
      return false;
    }

    if (hi - d < coarseStep) break;
    d = (uint16_t)(d + coarseStep);
  }

  if (!haveBest) return false;

  uint16_t fineStep = coarseStep / 4U;
  if (fineStep < 5) fineStep = 5;
  if (fineStep < coarseStep) {
    int32_t start = (int32_t)bestDutyX10 - (int32_t)coarseStep;
    int32_t stop = (int32_t)bestDutyX10 + (int32_t)coarseStep;
    if (start < (int32_t)lo) start = lo;
    if (stop > (int32_t)hi) stop = hi;

    for (uint16_t d = (uint16_t)start; d <= (uint16_t)stop; ) {
      setEnDutyX10(d);
      filtersPrimed = false;
      MeasureResult m = settleAndMeasure(cfg.autotuneSettleMs, cfg.autotuneMeasureMs);
      if (!considerFullTunePoint("FINE", d, targetV, m, loadSlot, bestDutyX10, bestV,
                                 bestErr, bestRipple, bestScore, haveBest)) {
        return false;
      }

      if ((uint16_t)stop - d < fineStep) break;
      d = (uint16_t)(d + fineStep);
    }
  }

  return true;
}

uint32_t autotuneFrequencyStepHz() {
  uint32_t lo = cfg.enFreqMinHz;
  uint32_t hi = cfg.enFreqMaxHz;
  if (hi <= lo) return 0;

  uint32_t span = hi - lo;
  uint32_t step = span / 5UL;
  if (step < 1000UL) step = 1000UL;
  if (step > 5000UL) step = 5000UL;
  if (step > span) step = span;
  return step;
}

uint32_t autotuneFullFrequencyStepHz() {
  uint32_t lo = cfg.enFreqMinHz;
  uint32_t hi = cfg.enFreqMaxHz;
  if (hi <= lo) return 0;

  uint32_t span = hi - lo;
  uint32_t step = span / 16UL;
  if (step < 1000UL) step = 1000UL;
  if (step > 2500UL) step = 2500UL;
  if (step > span) step = span;
  return step;
}

bool autotuneEvaluateFrequencyCandidate(uint32_t freqHz, float targetV,
                                        uint16_t &bestDutyX10, float &bestV,
                                        float &bestErr, float &bestRipple,
                                        uint32_t &bestFreqHz, float &bestScore,
                                        bool &haveBest) {
  freqHz = clampEnFreq(freqHz);
  setEnFrequencyHz(freqHz);

  CmdSerial.print("AUTOFREQ candidate ");
  CmdSerial.print(freqHz);
  CmdSerial.println(" Hz");

  uint16_t candDuty = cfg.biasDutyX10;
  float candV = 0.0f;
  float candErr = 99999.0f;
  float candRipple = 99999.0f;

  bool ok = autotuneFindDuty(targetV, candDuty, candV, candErr, candRipple);
  if (!ok) {
    if (faultLatched) return false;
    CmdSerial.println("AUTOFREQ candidate skipped: no valid duty point.");
    return true;
  }

  float score = candErr + (0.25f * candRipple);
  if (!haveBest || score < bestScore) {
    haveBest = true;
    bestScore = score;
    bestFreqHz = freqHz;
    bestDutyX10 = candDuty;
    bestV = candV;
    bestErr = candErr;
    bestRipple = candRipple;
  }

  CmdSerial.print("AUTOFREQ score=");
  CmdSerial.print(score, 4);
  CmdSerial.print(" best=");
  CmdSerial.print(bestFreqHz);
  CmdSerial.print(" Hz @ ");
  CmdSerial.print(dutyX10ToPercent(bestDutyX10), 2);
  CmdSerial.println(" %");
  return true;
}

bool autotuneFindFrequencyAndDuty(float targetV, uint16_t &bestDutyX10,
                                  float &bestV, float &bestErr,
                                  float &bestRipple, uint32_t &bestFreqHz) {
  CmdSerial.println("AUTOTUNE: EN frequency + duty search");
  CmdSerial.print("AUTOFREQ range=");
  CmdSerial.print(cfg.enFreqMinHz);
  CmdSerial.print("-");
  CmdSerial.print(cfg.enFreqMaxHz);
  CmdSerial.println(" Hz");

  uint32_t lo = cfg.enFreqMinHz;
  uint32_t hi = cfg.enFreqMaxHz;
  if (hi < lo) hi = lo;
  uint32_t step = autotuneFrequencyStepHz();

  float bestScore = 999999.0f;
  bool haveBest = false;
  uint32_t originalFreq = cfg.enFreqHz;

  if (!autotuneEvaluateFrequencyCandidate(originalFreq, targetV, bestDutyX10, bestV, bestErr,
                                          bestRipple, bestFreqHz, bestScore, haveBest)) {
    return false;
  }

  if (step == 0) {
    if (!haveBest) return false;
  } else {
    uint32_t f = lo;
    while (true) {
      if (!autotuneEvaluateFrequencyCandidate(f, targetV, bestDutyX10, bestV, bestErr,
                                              bestRipple, bestFreqHz, bestScore, haveBest)) {
        return false;
      }

      if (f >= hi) break;
      uint32_t next = f + step;
      if (next <= f || next > hi) next = hi;
      f = next;
    }
  }

  if (!haveBest) return false;

  setEnFrequencyHz(bestFreqHz);
  setEnDutyX10(bestDutyX10);
  CmdSerial.print("AUTOFREQ selected ");
  CmdSerial.print(bestFreqHz);
  CmdSerial.print(" Hz, duty ");
  CmdSerial.print(dutyX10ToPercent(bestDutyX10), 2);
  CmdSerial.print(" %, V=");
  CmdSerial.print(bestV, 3);
  CmdSerial.print(" V, error=");
  CmdSerial.print(bestErr, 3);
  CmdSerial.println(" V");
  return true;
}

bool autotuneEvaluateFullFrequencyCandidate(uint32_t freqHz, float targetV, int8_t loadSlot,
                                            uint16_t &bestDutyX10, float &bestV,
                                            float &bestErr, float &bestRipple,
                                            uint32_t &bestFreqHz, float &bestScore,
                                            bool &haveBest) {
  freqHz = clampEnFreq(freqHz);
  setEnFrequencyHz(freqHz);

  CmdSerial.print("AUTOFULL frequency ");
  CmdSerial.print(freqHz);
  CmdSerial.println(" Hz");

  uint16_t candDuty = cfg.biasDutyX10;
  float candV = 0.0f;
  float candErr = 99999.0f;
  float candRipple = 99999.0f;
  float candScore = 999999.0f;

  bool ok = autotuneFindDutyFull(targetV, loadSlot, candDuty, candV, candErr, candRipple, candScore);
  if (!ok) {
    if (faultLatched) return false;
    CmdSerial.println("AUTOFULL frequency skipped: no valid duty point.");
    return true;
  }

  if (!haveBest || candScore < bestScore) {
    haveBest = true;
    bestScore = candScore;
    bestFreqHz = freqHz;
    bestDutyX10 = candDuty;
    bestV = candV;
    bestErr = candErr;
    bestRipple = candRipple;
  }

  CmdSerial.print("AUTOFULL candidate score=");
  CmdSerial.print(candScore, 4);
  CmdSerial.print(" best=");
  CmdSerial.print(bestFreqHz);
  CmdSerial.print(" Hz @ ");
  CmdSerial.print(dutyX10ToPercent(bestDutyX10), 2);
  CmdSerial.println(" %");
  return true;
}

bool autotuneFindEverything(float targetV, int8_t loadSlot, uint16_t &bestDutyX10,
                            float &bestV, float &bestErr, float &bestRipple,
                            uint32_t &bestFreqHz) {
  CmdSerial.println("AUTOTUNE FULL: EN frequency + duty exhaustive search");
  CmdSerial.print("AUTOFULL range=");
  CmdSerial.print(cfg.enFreqMinHz);
  CmdSerial.print("-");
  CmdSerial.print(cfg.enFreqMaxHz);
  CmdSerial.println(" Hz");

  if (loadSlot >= 0 && validLoadSlot((uint8_t)loadSlot)) {
    CmdSerial.print("AUTOFULL load slot ");
    CmdSerial.print((int)loadSlot + 1);
    CmdSerial.print(": R=");
    CmdSerial.print(calLoadOhms((uint8_t)loadSlot), 3);
    CmdSerial.print(" ohm, expected I=");
    CmdSerial.print(expectedLoadCurrentA((uint8_t)loadSlot), 3);
    CmdSerial.print(" A, P=");
    CmdSerial.print(expectedLoadPowerW((uint8_t)loadSlot), 2);
    CmdSerial.println(" W");
  }

  uint32_t lo = cfg.enFreqMinHz;
  uint32_t hi = cfg.enFreqMaxHz;
  if (hi < lo) hi = lo;
  uint32_t step = autotuneFullFrequencyStepHz();

  float bestScore = 999999.0f;
  bool haveBest = false;
  uint32_t originalFreq = cfg.enFreqHz;

  if (!autotuneEvaluateFullFrequencyCandidate(originalFreq, targetV, loadSlot, bestDutyX10,
                                              bestV, bestErr, bestRipple, bestFreqHz,
                                              bestScore, haveBest)) {
    return false;
  }

  if (step == 0) {
    if (!haveBest) return false;
  } else {
    uint32_t f = lo;
    while (true) {
      if (!autotuneEvaluateFullFrequencyCandidate(f, targetV, loadSlot, bestDutyX10,
                                                  bestV, bestErr, bestRipple, bestFreqHz,
                                                  bestScore, haveBest)) {
        return false;
      }

      if (f >= hi) break;
      uint32_t next = f + step;
      if (next <= f || next > hi) next = hi;
      f = next;
    }
  }

  if (!haveBest) return false;

  setEnFrequencyHz(bestFreqHz);
  setEnDutyX10(bestDutyX10);
  CmdSerial.print("AUTOFULL selected ");
  CmdSerial.print(bestFreqHz);
  CmdSerial.print(" Hz, duty ");
  CmdSerial.print(dutyX10ToPercent(bestDutyX10), 2);
  CmdSerial.print(" %, V=");
  CmdSerial.print(bestV, 3);
  CmdSerial.print(" V, error=");
  CmdSerial.print(bestErr, 3);
  CmdSerial.print(" V, ripple=");
  CmdSerial.print(bestRipple, 3);
  CmdSerial.println(" V");
  return true;
}

bool autotuneIdentifyPlant(uint16_t baseDutyX10, float &gainVPerPct, float &tauS) {
  CmdSerial.println("AUTOTUNE: plant gain/tau estimate");
  gainVPerPct = 0.0f;
  tauS = 0.20f;

  setEnDutyX10(baseDutyX10);
  filtersPrimed = false;
  MeasureResult base = settleAndMeasure(400, 180);
  printMeasure("BASE", baseDutyX10, base);
  if (!base.valid || base.fault) return false;

  int16_t step = cfg.autotuneTestStepX10;
  if ((int32_t)baseDutyX10 + step > cfg.dutyMaxX10) step = -step;
  if ((int32_t)baseDutyX10 + step < cfg.dutyMinX10) step = cfg.autotuneTestStepX10;

  uint16_t stepDuty = clampDutyX10((int32_t)baseDutyX10 + step);
  if (stepDuty > cfg.dutyMaxX10) stepDuty = cfg.dutyMaxX10;
  if (stepDuty < cfg.dutyMinX10) stepDuty = cfg.dutyMinX10;
  float actualStepPct = (float)((int32_t)stepDuty - (int32_t)baseDutyX10) / 10.0f;
  if (fabsf(actualStepPct) < 0.2f) return false;

  const uint8_t MAX_SAMPLES = 80;
  float v[MAX_SAMPLES];
  float t[MAX_SAMPLES];
  uint8_t n = 0;

  setEnDutyX10(stepDuty);
  uint32_t startMs = millis();
  while (millis() - startMs < 600UL && n < MAX_SAMPLES) {
    bool needCurrentAdc = currentSenseAvailable();
    updateAnalogFilters(true, needCurrentAdc);
    if (checkFaults(true, needCurrentAdc)) return false;
    v[n] = latestVoutRaw;
    t[n] = ((float)(millis() - startMs)) / 1000.0f;
    n++;
    delay(5);
  }
  setEnDutyX10(baseDutyX10);

  if (n < 8) return false;
  float finalV = 0.0f;
  uint8_t count = 0;
  for (uint8_t i = (uint8_t)((n * 2) / 3); i < n; i++) {
    finalV += v[i];
    count++;
  }
  if (count == 0) count = 1;
  finalV /= (float)count;

  float deltaV = finalV - base.avgV;
  gainVPerPct = fabsf(deltaV / actualStepPct);
  if (gainVPerPct < 0.005f) {
    if (baseDutyX10 > 10 && base.avgV > 0.5f) gainVPerPct = base.avgV / dutyX10ToPercent(baseDutyX10);
  }
  if (gainVPerPct < 0.005f) gainVPerPct = 0.05f;

  float threshold = base.avgV + 0.632f * deltaV;
  bool found = false;
  for (uint8_t i = 0; i < n; i++) {
    if (actualStepPct > 0.0f) {
      if (v[i] >= threshold) { tauS = t[i]; found = true; break; }
    } else {
      if (v[i] <= threshold) { tauS = t[i]; found = true; break; }
    }
  }
  if (!found) tauS = 0.20f;
  tauS = clampFloat(tauS, 0.020f, 2.000f);

  CmdSerial.print("Plant gain="); CmdSerial.print(gainVPerPct, 5);
  CmdSerial.print(" V/%, tau="); CmdSerial.print(tauS, 3);
  CmdSerial.println(" s");
  return true;
}

void autotuneComputePI(float gainVPerPct, float tauS) {
  float lambda = 4.0f * tauS;
  lambda = clampFloat(lambda, 0.050f, 1.500f);

  float kp = tauS / (gainVPerPct * lambda);
  float ki = kp / tauS;

  // Extra conservatism for burst controlled LLC and load steps.
  kp *= 0.65f;
  ki *= 0.45f;

  kp = clampFloat(kp, 0.02f, 50.0f);
  ki = clampFloat(ki, 0.00f, 200.0f);

  cfg.kp_x1000 = (int32_t)(kp * 1000.0f + 0.5f);
  cfg.ki_x1000 = (int32_t)(ki * 1000.0f + 0.5f);
}

void autoTuneClosedLoop(bool fullScan, int8_t loadSlot) {
  if (autoTuneRunning) return;
  autoTuneRunning = true;

  CmdSerial.println();
  CmdSerial.println("================================================");
  CmdSerial.println(fullScan ? "AUTOTUNE FULL START: PA8/PA9 fixed, PA10 EN tries frequency/duty grid" :
                              "AUTOTUNE START: PA8/PA9 fixed, PA10 EN duty/frequency only");
  CmdSerial.println("================================================");

  systemEnabled = true;
  controlMode = MODE_OPEN_LOOP;
  faultLatched = false;
  faultCode = FAULT_NONE;
  sensorPowerupActive = false;
  maxDutyStartMs = 0;
  filtersPrimed = false;
  updateModeLEDs();
  setGateOutputsEnabled(true);
  setEnFrequencyHz(cfg.enFreqHz);

  float targetV = cfg.targetV;
  CmdSerial.print("Target="); CmdSerial.print(targetV, 3);
  CmdSerial.print(" V, ADC VREF="); CmdSerial.print(cfg.adcRefV, 3);
  CmdSerial.print(" V, divider="); CmdSerial.print(cfg.vdivTopK, 1);
  CmdSerial.print("k/"); CmdSerial.print(cfg.vdivBottomK, 1);
  CmdSerial.println("k");
  if (loadSlot >= 0 && validLoadSlot((uint8_t)loadSlot)) {
    cfg.activeCalLoadSlot = (uint8_t)loadSlot;
    CmdSerial.print("Calibration load slot ");
    CmdSerial.print((int)loadSlot + 1);
    CmdSerial.print(": R=");
    CmdSerial.print(calLoadOhms((uint8_t)loadSlot), 3);
    CmdSerial.print(" ohm, expected I=");
    CmdSerial.print(expectedLoadCurrentA((uint8_t)loadSlot), 3);
    CmdSerial.print(" A, expected P=");
    CmdSerial.print(expectedLoadPowerW((uint8_t)loadSlot), 2);
    CmdSerial.println(" W");
  }

  if (!autotunePowerSensor(targetV)) {
    setEnDutyX10(0);
    autoTuneRunning = false;
    CmdSerial.println("AUTOTUNE FAILED: voltage sensor did not become valid safely.");
    CmdSerial.print("> ");
    return;
  }

  uint16_t bestDuty = cfg.biasDutyX10;
  uint32_t bestFreq = cfg.enFreqHz;
  float bestV = 0.0f;
  float bestErr = 99999.0f;
  float bestRipple = 0.0f;
  bool searchOk = fullScan ?
    autotuneFindEverything(targetV, loadSlot, bestDuty, bestV, bestErr, bestRipple, bestFreq) :
    autotuneFindFrequencyAndDuty(targetV, bestDuty, bestV, bestErr, bestRipple, bestFreq);
  if (!searchOk) {
    setEnDutyX10(0);
    autoTuneRunning = false;
    CmdSerial.println(fullScan ? "AUTOTUNE FULL FAILED: exhaustive EN frequency/duty search failed." :
                                "AUTOTUNE FAILED: EN frequency/duty search failed.");
    CmdSerial.print("> ");
    return;
  }

  float gain = 0.0f;
  float tau = 0.20f;
  bool plantOk = autotuneIdentifyPlant(bestDuty, gain, tau);
  if (!plantOk) {
    CmdSerial.println("Plant ID weak; using conservative fallback from open-loop point.");
    gain = (bestDuty > 10 && bestV > 0.2f) ? bestV / dutyX10ToPercent(bestDuty) : 0.05f;
    if (gain < 0.005f) gain = 0.05f;
    tau = 0.20f;
  }

  autotuneComputePI(gain, tau);

  cfg.biasDutyX10 = bestDuty;
  cfg.enFreqHz = bestFreq;
  cfg.tunedDutyX10 = bestDuty;
  cfg.tunedTargetV = cfg.targetV;
  cfg.tunedPlantGainVPerPct = gain;
  cfg.tunedPlantTauS = tau;
  if (cfg.powerupDutyX10 > bestDuty && bestDuty > 10) cfg.powerupDutyX10 = bestDuty;
  if (loadSlot >= 0 && validLoadSlot((uint8_t)loadSlot)) {
    storeLoadProfile((uint8_t)loadSlot, bestFreq, bestDuty, gain, tau, bestV, filteredCurrent);
  }

  updateComparatorDacThreshold();

  CmdSerial.println("AUTOTUNE: entering closed loop");
  controlMode = MODE_CLOSED_LOOP;
  cfg.controlMode = MODE_CLOSED_LOOP;
  closedLoopIntegratorPct = 0.0f;
  controlDutyPercent = dutyX10ToPercent(bestDuty);
  comparatorDutyX10 = (float)bestDuty;
  setEnDutyX10(bestDuty);
  updateModeLEDs();

  saveSettings();

  CmdSerial.println();
  CmdSerial.println("AUTOTUNE RESULT");
  CmdSerial.print("EN frequency=");
  CmdSerial.print(bestFreq);
  CmdSerial.println(" Hz");
  CmdSerial.print("Bias duty="); CmdSerial.print(dutyX10ToPercent(bestDuty), 2); CmdSerial.println(" %");
  CmdSerial.print("Best open-loop V="); CmdSerial.print(bestV, 3); CmdSerial.print(" V, error="); CmdSerial.print(bestErr, 3); CmdSerial.println(" V");
  CmdSerial.print("Ripple band="); CmdSerial.print(bestRipple, 3); CmdSerial.println(" V");
  CmdSerial.print("Kp="); CmdSerial.print(((float)cfg.kp_x1000) / 1000.0f, 4);
  CmdSerial.print(" %/V, Ki="); CmdSerial.print(((float)cfg.ki_x1000) / 1000.0f, 4); CmdSerial.println(" %/(V*s)");
  CmdSerial.print("Plant gain="); CmdSerial.print(gain, 5); CmdSerial.print(" V/%, tau="); CmdSerial.print(tau, 3); CmdSerial.println(" s");
  if (loadSlot >= 0 && validLoadSlot((uint8_t)loadSlot)) {
    CmdSerial.print("Saved load slot ");
    CmdSerial.print((int)loadSlot + 1);
    CmdSerial.print(" profile: R=");
    CmdSerial.print(calLoadOhms((uint8_t)loadSlot), 3);
    CmdSerial.print(" ohm, expected I=");
    CmdSerial.print(expectedLoadCurrentA((uint8_t)loadSlot), 3);
    CmdSerial.print(" A, measured I=");
    CmdSerial.print(cfg.calLoadMeasuredI[(uint8_t)loadSlot], 3);
    CmdSerial.println(" A");
  }
  CmdSerial.print("ADC block last/max="); CmdSerial.print(lastAdcBlockUs); CmdSerial.print("/"); CmdSerial.print(maxAdcBlockUs); CmdSerial.println(" us");
  CmdSerial.println("AUTOTUNE COMPLETE. Settings saved.");
  CmdSerial.print("> ");

  autoTuneRunning = false;
}

void autoTuneClosedLoop() {
  autoTuneClosedLoop(false, -1);
}

// ============================================================
// UART status and params
// ============================================================

const char *feedbackName() {
  switch (feedbackPath) {
    case FB_SECONDARY_VOLTAGE: return "VOLTAGE";
    case FB_VOLTAGE_CURRENT: return "VOLTAGE+CURRENT";
    case FB_COMPARATOR: return "COMPARATOR";
    case FB_COMPARATOR_CURRENT: return "COMPARATOR+CURRENT";
    default: return "?";
  }
}

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

void printLiveStatusLine() {
  CmdSerial.print("\rVout="); CmdSerial.print(filteredVout, 3); CmdSerial.print("V");
  CmdSerial.print(" I="); CmdSerial.print(filteredCurrent, 3); CmdSerial.print("A");
  CmdSerial.print(" Dcmd="); CmdSerial.print(getCmdDutyPercent(), 1); CmdSerial.print("%");
  CmdSerial.print(" Deff="); CmdSerial.print(getEffDutyPercent(), 1); CmdSerial.print("%");
  CmdSerial.print(" FEN="); CmdSerial.print(enFreqRuntimeHz);
  CmdSerial.print("Hz FB="); CmdSerial.print(feedbackName());
  CmdSerial.print(" dt="); CmdSerial.print(lastControlDtUs); CmdSerial.print("us");
  CmdSerial.print(" ADC="); CmdSerial.print(lastAdcBlockUs); CmdSerial.print("us");
  if (compLastAbove && feedbackUsesComparator()) CmdSerial.print(" COMP=HI");
  if (!latestSensorValid) CmdSerial.print(" SENSOR?");
  if (latestSensorSaturated) CmdSerial.print(" ADC_SAT");
  if (sensorPowerupActive) CmdSerial.print(" PWRUP");
  if (faultLatched) { CmdSerial.print(" FAULT="); CmdSerial.print(faultName()); }
  CmdSerial.print("                              ");
}

void printParams() {
  CmdSerial.println();
  CmdSerial.println("SET-able parameters:");
  CmdSerial.println("TARGET, VREF, AMCREF, AMCVCLIP, RTOP, RBOT, VGAIN, VOFF, SENSORV");
  CmdSerial.println("FEN, FMIN, FMAX, MINEDGE, STATIC, DMIN, DMAX, OD, BIAS, PWRDUTY");
  CmdSerial.println("CPER, STATUSMS, ADCV, ADCI, ADCDUMMY, VTAU, ITAU");
  CmdSerial.println("KP, KI, DB, SLEW, IMIN, IMAX");
  CmdSerial.println("CSRES, CSGAIN, CSOFF, ITRIP, ITRIPEN, ISOFT, IFOLDEN, IFOLD, IDROOP");
  CmdSerial.println("OVPEN, OVP, MAXFAULTEN, MAXFAULTMS, MAXFAULTERR");
  CmdSerial.println("COMPRUP, COMPRDN, COMPOFF, COMPHYST");
  CmdSerial.println("AUTOMAX, AUTOSTEP, AUTOBIN, AUTOSETTLE, AUTOMEAS, AUTOTEST, LOAD1, LOAD2, LOAD3");
  CmdSerial.println("Examples: SET TARGET 12.0 | SET DMAX 95 | SET CPER 250 | FB 1 | CAL | AUTOFULL 1");
  CmdSerial.println("FB 0=secondary voltage, 1=secondary+primary current, 2=comparator, 3=comparator+current");
  CmdSerial.println("Autotune EN frequency search uses FMIN/FMAX. Set FMIN=FMAX to force one EN frequency.");
  CmdSerial.println("Load calibration: SET LOAD1 ohms, LOAD 1, CALLOAD 1, AUTOFULL 1, CAL3.");
}

void printStatus() {
  updateAnalogFilters(true, currentSenseAvailable());

  uint32_t arr, ccr1, ccr2, deadTicks, actualDeadNs;
  bool gateOk = calculateGateTiming(arr, ccr1, ccr2, deadTicks, actualDeadNs);

  CmdSerial.println();
  CmdSerial.println("========== LLC CONTROL STATUS ==========");
  CmdSerial.print("System: "); CmdSerial.println(systemEnabled ? "ON" : "OFF");
  CmdSerial.print("Mode: "); CmdSerial.println(controlMode == MODE_OPEN_LOOP ? "OPEN" : "CLOSED");
  CmdSerial.print("Feedback path: "); CmdSerial.println(feedbackName());
  CmdSerial.print("Command UART: "); CmdSerial.println(commandUartName());
  CmdSerial.print("PA2 current sense available: "); CmdSerial.println(currentSenseAvailable() ? "YES" : "NO");
  if (feedbackConfiguredForCurrent() && !currentSenseAvailable()) {
    CmdSerial.println("Current feedback requested but inactive because command UART reserves PA2.");
  }
  CmdSerial.print("Fault: "); CmdSerial.println(faultLatched ? faultName() : "NONE");

  CmdSerial.print("PA8/PA9 fixed: "); CmdSerial.print(GATE_FREQ_HZ); CmdSerial.print(" Hz, requested dead-time "); CmdSerial.print(GATE_DEADTIME_NS); CmdSerial.println(" ns");
  CmdSerial.print("PA8/PA9 carrier policy: ");
#if KEEP_GATE_PWM_RUNNING
  CmdSerial.println("kept running; PA10 EN is disabled for OFF/fault");
#else
  CmdSerial.println("TIM1 stopped when system is OFF/faulted");
#endif
  if (gateOk) {
    CmdSerial.print("TIM1 ARR/CCR1/CCR2: "); CmdSerial.print(arr); CmdSerial.print("/"); CmdSerial.print(ccr1); CmdSerial.print("/"); CmdSerial.println(ccr2);
    CmdSerial.print("Actual dead-time approx: "); CmdSerial.print(actualDeadNs); CmdSerial.println(" ns per timer tick request");
  }

  CmdSerial.print("PA10 EN freq/min/max: "); CmdSerial.print(enFreqRuntimeHz); CmdSerial.print(" / "); CmdSerial.print(cfg.enFreqMinHz); CmdSerial.print(" / "); CmdSerial.println(cfg.enFreqMaxHz);
  CmdSerial.print("PA10 duty cmd/effective/min/max: "); CmdSerial.print(getCmdDutyPercent(), 2); CmdSerial.print(" / "); CmdSerial.print(getEffDutyPercent(), 2); CmdSerial.print(" / "); CmdSerial.print(dutyX10ToPercent(cfg.dutyMinX10), 1); CmdSerial.print(" / "); CmdSerial.print(dutyX10ToPercent(cfg.dutyMaxX10), 1); CmdSerial.println(" %");
  CmdSerial.print("PA10 period/high/minedge/static100: "); CmdSerial.print(enPeriodUs); CmdSerial.print("/"); CmdSerial.print(enHighUs); CmdSerial.print("/"); CmdSerial.print(cfg.enMinEdgeUs); CmdSerial.print(" us / "); CmdSerial.println(cfg.allowStatic100 ? "YES" : "NO");
  CmdSerial.println("PA10 timing: TIM3 fixed-period update sets EN high; TIM3 compare sets EN low.");

  CmdSerial.print("Target/Bias/Open/PwrDuty: "); CmdSerial.print(cfg.targetV, 3); CmdSerial.print(" V / "); CmdSerial.print(dutyX10ToPercent(cfg.biasDutyX10), 2); CmdSerial.print("% / "); CmdSerial.print(dutyX10ToPercent(cfg.openLoopDutyX10), 2); CmdSerial.print("% / "); CmdSerial.print(dutyX10ToPercent(cfg.powerupDutyX10), 2); CmdSerial.println("%");
  CmdSerial.print("Kp/Ki/deadband/slew: "); CmdSerial.print(((float)cfg.kp_x1000) / 1000.0f, 4); CmdSerial.print(" / "); CmdSerial.print(((float)cfg.ki_x1000) / 1000.0f, 4); CmdSerial.print(" / "); CmdSerial.print(cfg.deadbandMv); CmdSerial.print(" mV / "); CmdSerial.print(((float)cfg.slewX10PerSec) / 10.0f); CmdSerial.println(" %/s");

  CmdSerial.print("ADC VREF/AMCREF/AMCVCLIP: "); CmdSerial.print(cfg.adcRefV, 4); CmdSerial.print(" / "); CmdSerial.print(cfg.amcRefV, 4); CmdSerial.print(" / "); CmdSerial.println(cfg.amcVclipV, 4);
  CmdSerial.print("Divider top/bottom/ratio: "); CmdSerial.print(cfg.vdivTopK, 2); CmdSerial.print("k / "); CmdSerial.print(cfg.vdivBottomK, 2); CmdSerial.print("k / "); CmdSerial.println(dividerRatio(), 6);
  CmdSerial.print("PA1 raw ADC/V: "); CmdSerial.print(rawPa1Adc); CmdSerial.print(" / "); CmdSerial.print(rawPa1Voltage, 5); CmdSerial.println(" V");
  CmdSerial.print("Vout raw/filtered valid/sat: "); CmdSerial.print(latestVoutRaw, 4); CmdSerial.print(" / "); CmdSerial.print(filteredVout, 4); CmdSerial.print(" V / "); CmdSerial.print(latestSensorValid ? "YES" : "NO"); CmdSerial.print(" / "); CmdSerial.println(latestSensorSaturated ? "YES" : "NO");

  CmdSerial.print("Current CSRES/CSGAIN/offset: "); CmdSerial.print(cfg.csResOhms, 2); CmdSerial.print(" ohm / "); CmdSerial.print(cfg.csGainAperA, 6); CmdSerial.print(" A/A / "); CmdSerial.print(cfg.currentOffsetV, 5); CmdSerial.println(" V");
  CmdSerial.print("PA2 raw ADC/V: "); CmdSerial.print(rawPa2Adc); CmdSerial.print(" / "); CmdSerial.print(rawPa2Voltage, 5); CmdSerial.println(" V");
  CmdSerial.print("Current raw/filtered trip/soft: "); CmdSerial.print(latestCurrentRaw, 4); CmdSerial.print(" / "); CmdSerial.print(filteredCurrent, 4); CmdSerial.print(" A / "); CmdSerial.print(cfg.currentTripA, 2); CmdSerial.print(" / "); CmdSerial.println(cfg.currentSoftA, 2);

  CmdSerial.print("Control period range/requested/last/max/overruns: ");
  CmdSerial.print(CONTROL_PERIOD_MIN_HARD_US); CmdSerial.print("-");
  CmdSerial.print(CONTROL_PERIOD_MAX_HARD_US); CmdSerial.print(" / ");
  CmdSerial.print(cfg.controlPeriodUs); CmdSerial.print(" / "); CmdSerial.print(lastControlDtUs); CmdSerial.print(" / "); CmdSerial.print(maxControlDtUs); CmdSerial.print(" us / "); CmdSerial.println(controlOverrunCount);
  CmdSerial.print("ADC block last/max: "); CmdSerial.print(lastAdcBlockUs); CmdSerial.print(" / "); CmdSerial.print(maxAdcBlockUs); CmdSerial.println(" us");

  CmdSerial.print("Comparator configured/DAC code/above: "); CmdSerial.print(comparatorConfigured ? "YES" : "NO"); CmdSerial.print(" / "); CmdSerial.print(compDacCode); CmdSerial.print(" / "); CmdSerial.println(compLastAbove ? "YES" : "NO");

  CmdSerial.print("Tuned duty/target/gain/tau: "); CmdSerial.print(dutyX10ToPercent(cfg.tunedDutyX10), 2); CmdSerial.print("% / "); CmdSerial.print(cfg.tunedTargetV, 3); CmdSerial.print(" V / "); CmdSerial.print(cfg.tunedPlantGainVPerPct, 5); CmdSerial.print(" V/% / "); CmdSerial.print(cfg.tunedPlantTauS, 3); CmdSerial.println(" s");
  CmdSerial.print("Active load slot: "); CmdSerial.println((int)cfg.activeCalLoadSlot + 1);
  for (uint8_t i = 0; i < CAL_LOAD_SLOT_COUNT; i++) {
    CmdSerial.print("LOAD"); CmdSerial.print((int)i + 1);
    CmdSerial.print(": R="); CmdSerial.print(calLoadOhms(i), 3);
    CmdSerial.print(" ohm expI="); CmdSerial.print(expectedLoadCurrentA(i), 3);
    CmdSerial.print(" A expP="); CmdSerial.print(expectedLoadPowerW(i), 2);
    CmdSerial.print(" W");
    if (loadProfileValid(i)) {
      CmdSerial.print(" tuned FEN="); CmdSerial.print(cfg.calLoadFreqHz[i]);
      CmdSerial.print("Hz BIAS="); CmdSerial.print(dutyX10ToPercent(cfg.calLoadDutyX10[i]), 2);
      CmdSerial.print("% KP="); CmdSerial.print(((float)cfg.calLoadKp_x1000[i]) / 1000.0f, 4);
      CmdSerial.print(" KI="); CmdSerial.print(((float)cfg.calLoadKi_x1000[i]) / 1000.0f, 4);
      CmdSerial.print(" Vmeas="); CmdSerial.print(cfg.calLoadMeasuredV[i], 3);
      CmdSerial.print(" Imeas="); CmdSerial.print(cfg.calLoadMeasuredI[i], 3);
    } else {
      CmdSerial.print(" not tuned");
    }
    CmdSerial.println();
  }
  CmdSerial.print("EEPROM slot/seq: "); CmdSerial.print(activeSlotIndex); CmdSerial.print(" / "); CmdSerial.println(settingsSequence);
  printParams();
  CmdSerial.println("========================================");
}

// ============================================================
// UART parser
// ============================================================

bool parseSetParam(String name, float value) {
  name.trim();
  name.toUpperCase();

  if (name == "TARGET" || name == "V") cfg.targetV = clampFloat(value, TARGET_MIN_V, TARGET_MAX_V);
  else if (name == "VREF") cfg.adcRefV = clampFloat(value, 1.0f, 3.6f);
  else if (name == "AMCREF") cfg.amcRefV = clampFloat(value, 1.0f, 5.0f);
  else if (name == "AMCVCLIP") cfg.amcVclipV = clampFloat(value, 0.5f, 3.0f);
  else if (name == "RTOP") cfg.vdivTopK = clampFloat(value, 1.0f, 10000.0f);
  else if (name == "RBOT") cfg.vdivBottomK = clampFloat(value, 0.1f, 1000.0f);
  else if (name == "VGAIN") cfg.voutGain = clampFloat(value, 0.1f, 10.0f);
  else if (name == "VOFF") cfg.voutOffsetV = clampFloat(value, -20.0f, 20.0f);
  else if (name == "SENSORV") cfg.sensorMinPa1V = clampFloat(value, 0.0f, 2.0f);

  else if (name == "FEN" || name == "E") cfg.enFreqHz = clampU32((uint32_t)value, cfg.enFreqMinHz, cfg.enFreqMaxHz);
  else if (name == "FMIN") cfg.enFreqMinHz = clampU32((uint32_t)value, EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
  else if (name == "FMAX") cfg.enFreqMaxHz = clampU32((uint32_t)value, EN_FREQ_MIN_HARD_HZ, EN_FREQ_MAX_HARD_HZ);
  else if (name == "MINEDGE") cfg.enMinEdgeUs = (uint16_t)clampU32((uint32_t)value, EN_MIN_EDGE_HARD_US, EN_MAX_EDGE_HARD_US);
  else if (name == "STATIC") cfg.allowStatic100 = (value >= 0.5f) ? 1 : 0;
  else if (name == "DMIN") cfg.dutyMinX10 = dutyPercentToX10(value);
  else if (name == "DMAX") cfg.dutyMaxX10 = dutyPercentToX10(value);
  else if (name == "OD" || name == "D") cfg.openLoopDutyX10 = dutyPercentToX10(value);
  else if (name == "BIAS" || name == "B") cfg.biasDutyX10 = dutyPercentToX10(value);
  else if (name == "PWRDUTY" || name == "P") cfg.powerupDutyX10 = dutyPercentToX10(value);

  else if (name == "CPER") cfg.controlPeriodUs = clampU32((uint32_t)value, CONTROL_PERIOD_MIN_HARD_US, CONTROL_PERIOD_MAX_HARD_US);
  else if (name == "STATUSMS") cfg.statusMs = clampU32((uint32_t)value, 100UL, 5000UL);
  else if (name == "ADCV") cfg.adcVSamples = (uint16_t)clampU32((uint32_t)value, 1, 64);
  else if (name == "ADCI") cfg.adcISamples = (uint16_t)clampU32((uint32_t)value, 1, 64);
  else if (name == "ADCDUMMY") cfg.adcDummy = (uint16_t)clampU32((uint32_t)value, 0, 8);
  else if (name == "VTAU") cfg.voutTauMs = clampFloat(value, 0.1f, 500.0f);
  else if (name == "ITAU") cfg.currentTauMs = clampFloat(value, 0.1f, 500.0f);

  else if (name == "KP") cfg.kp_x1000 = (int32_t)(clampFloat(value, 0.0f, 50.0f) * 1000.0f + 0.5f);
  else if (name == "KI") cfg.ki_x1000 = (int32_t)(clampFloat(value, 0.0f, 200.0f) * 1000.0f + 0.5f);
  else if (name == "DB") cfg.deadbandMv = (int32_t)clampI32((int32_t)value, 0, 2000);
  else if (name == "SLEW") cfg.slewX10PerSec = (int32_t)(clampFloat(value, 0.1f, 2000.0f) * 10.0f + 0.5f);
  else if (name == "IMIN") cfg.integralMinX10 = (int32_t)(clampFloat(value, -100.0f, 100.0f) * 10.0f);
  else if (name == "IMAX") cfg.integralMaxX10 = (int32_t)(clampFloat(value, -100.0f, 100.0f) * 10.0f);

  else if (name == "CSRES") cfg.csResOhms = clampFloat(value, 1.0f, 10000.0f);
  else if (name == "CSGAIN") cfg.csGainAperA = clampFloat(value, 0.000001f, 0.1f);
  else if (name == "CSOFF") cfg.currentOffsetV = clampFloat(value, -1.0f, 1.0f);
  else if (name == "ITRIP") cfg.currentTripA = clampFloat(value, 0.1f, 100.0f);
  else if (name == "ITRIPEN") cfg.currentTripEnable = (value >= 0.5f) ? 1 : 0;
  else if (name == "ISOFT") cfg.currentSoftA = clampFloat(value, 0.0f, 100.0f);
  else if (name == "IFOLDEN") cfg.currentFoldbackEnable = (value >= 0.5f) ? 1 : 0;
  else if (name == "IFOLD") cfg.currentFoldPctPerA = clampFloat(value, 0.0f, 100.0f);
  else if (name == "IDROOP") cfg.currentDroopVPerA = clampFloat(value, 0.0f, 10.0f);

  else if (name == "OVPEN") cfg.ovpEnable = (value >= 0.5f) ? 1 : 0;
  else if (name == "OVP") cfg.ovpV = clampFloat(value, TARGET_MIN_V, 80.0f);
  else if (name == "MAXFAULTEN") cfg.maxDutyFaultEnable = (value >= 0.5f) ? 1 : 0;
  else if (name == "MAXFAULTMS") cfg.maxDutyFaultMs = clampU32((uint32_t)value, 50UL, 10000UL);
  else if (name == "MAXFAULTERR") cfg.maxDutyFaultErrMv = clampI32((int32_t)value, 0, 10000);

  else if (name == "COMPRUP") cfg.compRampUpX10PerSec = (int32_t)(clampFloat(value, 0.1f, 2000.0f) * 10.0f + 0.5f);
  else if (name == "COMPRDN") cfg.compRampDownX10PerSec = (int32_t)(clampFloat(value, 0.1f, 2000.0f) * 10.0f + 0.5f);
  else if (name == "COMPOFF") cfg.compDacOffsetMv = clampI32((int32_t)value, -1000, 1000);
  else if (name == "COMPHYST") cfg.compHystCode = (uint8_t)clampU32((uint32_t)value, 0, 3);

  else if (name == "AUTOMAX") cfg.autotuneMaxDutyX10 = dutyPercentToX10(value);
  else if (name == "AUTOSTEP") cfg.autotuneCoarseStepX10 = (uint16_t)clampU32((uint32_t)(value * 10.0f + 0.5f), 5, 200);
  else if (name == "AUTOBIN") cfg.autotuneBinarySteps = (uint8_t)clampU32((uint32_t)value, 3, 12);
  else if (name == "AUTOSETTLE") cfg.autotuneSettleMs = clampU32((uint32_t)value, 20, 3000);
  else if (name == "AUTOMEAS") cfg.autotuneMeasureMs = clampU32((uint32_t)value, 20, 2000);
  else if (name == "AUTOTEST") cfg.autotuneTestStepX10 = (uint16_t)clampU32((uint32_t)(value * 10.0f + 0.5f), 5, 100);
  else if (name == "LOAD1" || name == "RLOAD1") cfg.calLoadOhms[0] = clampFloat(value, 0.0f, 100000.0f);
  else if (name == "LOAD2" || name == "RLOAD2") cfg.calLoadOhms[1] = clampFloat(value, 0.0f, 100000.0f);
  else if (name == "LOAD3" || name == "RLOAD3") cfg.calLoadOhms[2] = clampFloat(value, 0.0f, 100000.0f);
  else return false;

  validateSettings();
  setEnFrequencyHz(cfg.enFreqHz);
  if (controlMode == MODE_OPEN_LOOP) setEnDutyX10(cfg.openLoopDutyX10);
  if (feedbackUsesComparator()) setupComparatorHardware();
  saveSettings();
  return true;
}

void zeroCurrentOffset() {
  if (!currentSenseAvailable()) {
    CmdSerial.println("Current offset not changed: PA2 current ADC is disabled while using ST-LINK Serial.");
    return;
  }

  float sum = 0.0f;
  for (int i = 0; i < 64; i++) {
    rawPa2Adc = readAdcAveragedFast(SENSE_CURRENT_PIN, 1);
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
  CmdSerial.println("Use LOAD 1..3, CALLOAD 1..3, AUTOFULL 1..3, or SET LOAD1/2/3 ohms.");
}

int8_t waitForLoadGo(uint8_t slot) {
  CmdSerial.println();
  CmdSerial.print("Install calibration LOAD");
  CmdSerial.print((int)slot + 1);
  CmdSerial.print(" = ");
  CmdSerial.print(calLoadOhms(slot), 3);
  CmdSerial.print(" ohm, then type GO. Type SKIP or ABORT instead.");
  CmdSerial.println();
  CmdSerial.print("> ");

  String line;
  while (true) {
    while (CmdSerial.available()) {
      char c = CmdSerial.read();
      if (c == '\r') continue;
      if (c == '\n') {
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
        if (line.length() > 0) {
          line.remove(line.length() - 1);
          CmdSerial.print("\b \b");
        }
      } else {
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

    autoTuneClosedLoop(true, (int8_t)slot);
    setSystemEnabled(false, true);
  }

  CmdSerial.println("CAL3 complete. Use LOAD 1..3 to apply a saved load profile.");
  CmdSerial.print("> ");
}

void processCommand(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;

  String up = cmd;
  up.toUpperCase();

  if (up == "?" || up == "STATUS") { printStatus(); return; }
  if (up == "PARAMS") { printParams(); return; }
  if (up == "ON") { setSystemEnabled(true, true); CmdSerial.println("System ON"); return; }
  if (up == "OFF") { setSystemEnabled(false, true); CmdSerial.println("System OFF"); return; }
  if (up == "MO" || up == "OPEN") { setMode(MODE_OPEN_LOOP, true); CmdSerial.println("OPEN LOOP"); return; }
  if (up == "MC" || up == "CLOSED") { setMode(MODE_CLOSED_LOOP, true); CmdSerial.println("CLOSED LOOP"); return; }
  if (up == "CAL" || up == "AUTOTUNE") { autoTuneClosedLoop(false, -1); return; }
  if (up == "CAL3") { autoTuneThreeLoads(); return; }
  if (up.startsWith("CALLOAD")) {
    int8_t slot = parseLoadSlotText(up.substring(7));
    if (slot < 0) { printLoadCommandHelp(); return; }
    autoTuneClosedLoop(true, slot);
    return;
  }
  if (up.startsWith("AUTOFULL") || up.startsWith("CALFULL")) {
    uint8_t prefixLen = up.startsWith("AUTOFULL") ? 8 : 7;
    int8_t slot = parseLoadSlotText(up.substring(prefixLen));
    if (slot < 0) { printLoadCommandHelp(); return; }
    autoTuneClosedLoop(true, slot);
    return;
  }
  if (up == "SAVE") { saveSettings(); CmdSerial.println("Saved."); return; }
  if (up == "DEFAULTS") { setDefaults(); validateSettings(); saveSettings(); applyModeState(false); CmdSerial.println("Defaults restored and saved."); return; }
  if (up == "CLR") { faultLatched = false; faultCode = FAULT_NONE; setGateOutputsEnabled(systemEnabled); applyModeState(false); CmdSerial.println("Fault cleared."); return; }
  if (up == "ZEROI" || up == "IZERO") { zeroCurrentOffset(); return; }
  if (up == "FAST") { cfg.controlPeriodUs = 250; cfg.adcVSamples = 2; cfg.adcISamples = 1; cfg.voutTauMs = 1.5f; cfg.currentTauMs = 1.0f; saveSettings(); CmdSerial.println("Fast loop preset saved: 250 us control period. Use SET CPER 100..20000 to tune."); return; }
  if (up == "SAFE") { cfg.dutyMaxX10 = 900; cfg.allowStatic100 = 0; cfg.maxDutyFaultEnable = 1; cfg.currentTripEnable = 1; saveSettings(); CmdSerial.println("Safe preset saved."); return; }

  if (up.startsWith("LOAD")) {
    int8_t slot = parseLoadSlotText(up.substring(4));
    if (slot < 0) { printLoadCommandHelp(); return; }
    applyLoadProfile((uint8_t)slot, true);
    CmdSerial.print("Active load slot ");
    CmdSerial.print((int)slot + 1);
    CmdSerial.print(" selected, R=");
    CmdSerial.print(calLoadOhms((uint8_t)slot), 3);
    CmdSerial.println(" ohm.");
    if (loadProfileValid((uint8_t)slot)) {
      CmdSerial.print("Applied tuned profile: FEN=");
      CmdSerial.print(cfg.calLoadFreqHz[(uint8_t)slot]);
      CmdSerial.print(" Hz, BIAS=");
      CmdSerial.print(dutyX10ToPercent(cfg.calLoadDutyX10[(uint8_t)slot]), 2);
      CmdSerial.println(" %.");
    } else {
      CmdSerial.println("No saved tune for this load slot yet.");
    }
    return;
  }

  if (up.startsWith("FB")) {
    String rest = up.substring(2); rest.trim();
    int p = rest.toInt();
    if (p < 0 || p > 3) {
      CmdSerial.println("Use FB 0 voltage, FB 1 voltage+current, FB 2 comparator, FB 3 comparator+current.");
      return;
    }
    setFeedbackPath((FeedbackPath)p, true);
    CmdSerial.print("Feedback path set to "); CmdSerial.println(feedbackName());
    if (feedbackConfiguredForCurrent() && !currentSenseAvailable()) {
      CmdSerial.println("Warning: PA2 current feedback is inactive while using ST-LINK Serial. Use PC5/PC4 command UART to enable it.");
    }
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
    val.trim();
    float f = val.toFloat();
    if (parseSetParam(name, f)) {
      CmdSerial.print("Set "); CmdSerial.print(name); CmdSerial.print(" = "); CmdSerial.println(f, 6);
    } else {
      CmdSerial.println("Unknown parameter. Type PARAMS.");
    }
    return;
  }

  if (up.startsWith("KP")) {
    String rest = up.substring(2); rest.trim();
    if (parseSetParam("KP", rest.toFloat())) CmdSerial.println("Kp saved.");
    return;
  }
  if (up.startsWith("KI")) {
    String rest = up.substring(2); rest.trim();
    if (parseSetParam("KI", rest.toFloat())) CmdSerial.println("Ki saved.");
    return;
  }

  // Short aliases from original workflow.
  char c = up.charAt(0);
  String val = up.substring(1);
  val.trim();
  if (c == 'D') {
    if (parseSetParam("OD", val.toFloat())) CmdSerial.println("Open-loop duty saved.");
    return;
  }
  if (c == 'E') {
    if (parseSetParam("FEN", val.toFloat())) CmdSerial.println("EN frequency saved.");
    return;
  }
  if (c == 'V') {
    if (parseSetParam("TARGET", val.toFloat())) CmdSerial.println("Target saved.");
    return;
  }
  if (c == 'B') {
    if (parseSetParam("BIAS", val.toFloat())) CmdSerial.println("Bias saved.");
    return;
  }
  if (c == 'P') {
    if (parseSetParam("PWRDUTY", val.toFloat())) CmdSerial.println("Power-up duty saved.");
    return;
  }

  CmdSerial.println("Unknown command. Type ? or PARAMS.");
}

void handleSerial() {
  static String input = "";

  while (CmdSerial.available()) {
    char c = CmdSerial.read();

    if (!uartInputActive) {
      CmdSerial.println();
      CmdSerial.print("> ");
      uartInputActive = true;
    }

    if (c == '\b' || c == 127) {
      if (input.length() > 0) {
        input.remove(input.length() - 1);
        CmdSerial.print("\b \b");
      }
    } else if (c == '\n' || c == '\r') {
      CmdSerial.println();
      if (input.length() > 0) {
        processCommand(input);
        input = "";
      }
      uartInputActive = false;
      CmdSerial.print("> ");
    } else {
      input += c;
      CmdSerial.write(c);
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

  pinMode(SENSE_VOUT_PIN, INPUT_ANALOG);
#if !(CMD_UART_USE_ARDUINO_SERIAL && CMD_UART_SERIAL_USES_PA2)
  pinMode(SENSE_CURRENT_PIN, INPUT_ANALOG);
#endif
  pinMode(COMP_DAC_PIN, INPUT_ANALOG);

  analogReadResolution(ADC_RESOLUTION_BITS);
  analogWriteResolution(12);

  EEPROM.begin();
  loadSettings();

  setupEnablePWM();
  setupGatePWM();
  if (feedbackUsesComparator()) setupComparatorHardware();

  applyModeState(false);

  for (uint8_t i = 0; i < 20; i++) {
    updateAnalogFilters(true, currentSenseAvailable());
    delay(2);
  }

  CmdSerial.println();
  CmdSerial.println("STM32G071 LLC closed-loop firmware loaded");
  CmdSerial.print("Command UART: ");
  CmdSerial.println(commandUartName());
#if CMD_UART_USE_ARDUINO_SERIAL && CMD_UART_SERIAL_USES_PA2
  CmdSerial.println("PA2 current ADC is disabled while using ST-LINK Serial. Set CMD_UART_USE_ARDUINO_SERIAL=0 for PC5/PC4 UART and current feedback.");
#endif
  CmdSerial.println("Fixed PA8/PA9: 1 MHz, requested 40 ns dead-time. Control actuator: PA10 EN only.");
  CmdSerial.println("Default scaling: VREF=3.3 V, secondary divider 390k/10k, current CS pulldown 820 ohm.");
  CmdSerial.println("Type ? for status, PARAMS for tunables, CAL for autotune.");
  printStatus();
  CmdSerial.print("> ");
}

void loop() {
  handleSerial();

  if (systemEnabled && !autoTuneRunning) {
    handleClosedLoopControl();
  }

  // Background sampling for status in open loop / off. Closed loop samples inside its controller.
  static uint32_t lastBgUs = 0;
  uint32_t nowUs = micros();
  if (!autoTuneRunning && (nowUs - lastBgUs >= 2000UL)) {
    lastBgUs = nowUs;
    if (!systemEnabled || controlMode == MODE_OPEN_LOOP) {
      bool needCurrentAdc = currentSenseAvailable();
      updateAnalogFilters(true, needCurrentAdc);
      checkFaults(true, needCurrentAdc);
    }
  }

  static uint32_t lastStatus = 0;
  if (!uartInputActive && !autoTuneRunning && millis() - lastStatus >= cfg.statusMs) {
    lastStatus = millis();
    printLiveStatusLine();
  }
}
