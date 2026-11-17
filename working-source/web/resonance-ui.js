import { analyzeTank, analyzeMagnetizingBranch, analyzePump, equivalentCapacitance, preferredCandidates, resonanceFrequency } from './resonance.js';
import { PRESETS, SOURCES, TRANSFORMER_REFERENCES } from './resonance-presets.js';

const $ = (id) => document.getElementById(id);
const scale = { pF: 1e-12, nF: 1e-9, uF: 1e-6, kHz: 1e3, MHz: 1e6 };
const form = $('tank-form');
const canvas = $('response-chart');
let selectedPreset = null;
let modified = false;
let currentCalculation = null;
let recordRows = [];
let currentPumpCalculation = null;
const transformerReference = () => TRANSFORMER_REFERENCES.find((reference) => reference.id === $('transformer-reference').value) || null;
function sourceIds() {
  return [...new Set([...(selectedPreset?.sourceIds || []), ...($('magnetizing-inductance').value.trim() || transformerReference() ? ['thesisMagnetics'] : [])])];
}

function number(value, digits = 4) {
  if (!Number.isFinite(value)) return '—';
  if (value === 0) return '0';
  return Number(value.toPrecision(digits)).toString();
}

function quantity(value, kind, digits = 4) {
  if (!Number.isFinite(value)) return '—';
  const units = kind === 'frequency' ? [[1e6, 'MHz'], [1e3, 'kHz'], [1, 'Hz']]
    : kind === 'inductance' ? [[1, 'H'], [1e-3, 'mH'], [1e-6, 'µH'], [1e-9, 'nH']]
      : kind === 'capacitance' ? [[1, 'F'], [1e-3, 'mF'], [1e-6, 'µF'], [1e-9, 'nF'], [1e-12, 'pF']]
        : [[1, 'Ω']];
  const unit = units.find(([factor]) => Math.abs(value) >= factor) || units[units.length - 1];
  return `${number(value / unit[0], digits)} ${unit[1]}`;
}

function metric(id, value, kind) {
  const output = $(id);
  const text = quantity(value, kind);
  output.replaceChildren();
  if (text === '—') { output.textContent = text; return; }
  const split = text.lastIndexOf(' ');
  output.append(document.createTextNode(text.slice(0, split)));
  const unit = document.createElement('span');
  unit.className = 'unit';
  unit.textContent = text.slice(split + 1);
  output.append(unit);
}

function markFieldInvalid(id, message) {
  const input = $(id);
  input.setAttribute('aria-invalid', 'true');
  const advanced = input.closest('details');
  if (advanced) advanced.open = true;
  const feedback = $(`validation-${id}`);
  if (feedback) { feedback.textContent = message; feedback.hidden = false; }
}

function invalid(id, message) {
  markFieldInvalid(id, message);
  throw new Error(message);
}

function clearValidation(scope) {
  for (const input of scope.querySelectorAll('[aria-invalid]')) input.removeAttribute('aria-invalid');
  for (const feedback of scope.querySelectorAll('.field-error')) feedback.hidden = true;
}

function numeric(id, label, { optional = false, zero = false, max = Infinity } = {}) {
  const raw = $(id).value.trim();
  if (!raw && optional) return null;
  if (!raw) invalid(id, `${label} is required.`);
  const value = Number(raw);
  if (!Number.isFinite(value) || (zero ? value < 0 : value <= 0) || value > max) {
    invalid(id, `${label} must be ${zero ? 'zero or a positive number' : 'a positive number'}${Number.isFinite(max) ? ` no greater than ${max}` : ''}.`);
  }
  return value;
}

function readBank(required = true) {
  const raw = $('capacitor-values').value.trim();
  const values = raw.split(/[,;]/).map((value) => Number(value.trim()));
  if (!raw || values.some((value) => !Number.isFinite(value) || value <= 0)) {
    if (!required) return null;
    invalid('capacitor-values', !raw && selectedPreset?.capacitorBasis === 'unprovided' ? 'C26 has no value in this drawing. Enter the fitted or measured equivalent capacitance.' : 'Enter a positive equivalent capacitance, or positive bank values separated by commas.');
  }
  return values.map((value) => value * scale[$('capacitor-unit').value]);
}

function setText(id, text) { $(id).textContent = text; }

function updateSolveControls() {
  const solveFor = $('solve-for').value;
  const solveFrequency = solveFor === 'frequency';
  const solveL = solveFor === 'inductance';
  const solveC = solveFor === 'capacitance';
  $('target-frequency').disabled = solveFrequency;
  $('target-frequency-unit').disabled = solveFrequency;
  $('discrete-inductance').disabled = solveL;
  ['capacitor-values', 'capacitor-unit', 'capacitor-connection'].forEach((id) => { $(id).disabled = solveC; });
  setText('solve-note', solveFrequency ? 'Frequency is calculated from total series L and the capacitor bank.'
    : solveL ? 'Solve discrete L after subtracting the entered transformer leakage.'
      : 'Solve the required equivalent C. This does not select or replace physical capacitors.');
  $('result-frequency').classList.toggle('output-computed', solveFrequency);
  $('result-inductance').classList.toggle('output-computed', solveL);
  $('result-capacitance').classList.toggle('output-computed', solveC);
  setText('result-status', solveFrequency ? 'SOLVING fᵣ' : solveL ? 'SOLVING DISCRETE L' : 'SOLVING EQUIVALENT C');
  return solveFor;
}

function renderSource() {
  if (!selectedPreset) return;
  setText('preset-description', selectedPreset.description || 'Documented resonant tank values.');
  const assumed = selectedPreset.capacitorBasis === 'assumed-equivalent';
  const incomplete = selectedPreset.capacitorBasis === 'unprovided';
  setText('preset-state', modified ? 'MODIFIED INPUTS' : assumed ? 'ASSUMED SCENARIO' : incomplete ? 'DRAWING · VALUES MISSING' : 'DOCUMENT BASELINE');
  $('preset-state').className = `badge ${modified || assumed || incomplete ? 'demo' : 'neutral'}`;
  setText('preset-note', modified ? 'Source retained as a reference.' : assumed ? 'Borrowed values; verify the assembly.' : incomplete ? 'Complete the missing circuit values.' : 'Nominal values from the cited source.');
  setText('source-provenance', selectedPreset.sourceNote || selectedPreset.description || selectedPreset.label);
  const list = $('source-list');
  list.replaceChildren();
  for (const sourceId of sourceIds()) {
    const source = SOURCES[sourceId];
    const item = document.createElement('li');
    const title = document.createElement(source?.url && /^https?:\/\//.test(source.url) ? 'a' : 'strong');
    title.textContent = source?.title || sourceId;
    if (title.tagName === 'A') { title.href = source.url; title.target = '_blank'; title.rel = 'noopener noreferrer'; }
    item.append(title);
    if (source?.detail) {
      const detail = document.createElement('span');
      detail.className = 'source-detail';
      detail.textContent = source.detail;
      item.append(detail);
    }
    list.append(item);
  }
}

function warningsList(warnings) {
  const list = $('calculation-warnings');
  list.replaceChildren();
  for (const message of [...new Set(warnings)]) {
    const item = document.createElement('li');
    item.textContent = typeof message === 'string' ? message : message.message || String(message);
    list.append(item);
  }
}

function readInputs(solveFor) {
  const bank = readBank(solveFor !== 'capacitance');
  const leakageValue = numeric('leakage-inductance', 'Transformer leakage', { optional: true, zero: true });
  const resistance = numeric('series-resistance', 'Series resistance', { optional: true, zero: true });
  const enteredL = solveFor === 'inductance' ? null : numeric('discrete-inductance', 'Discrete inductance', { zero: true });
  const inputs = {
    solveFor,
    targetFrequencyHz: solveFor === 'frequency' ? null : numeric('target-frequency', 'Target resonance') * scale[$('target-frequency-unit').value],
    discreteInductanceH: enteredL === null ? null : enteredL * 1e-6,
    leakageInductanceH: (leakageValue ?? 0) * 1e-6,
    magnetizingInductanceH: (() => { const value = numeric('magnetizing-inductance', 'Magnetizing inductance', { optional: true }); return value === null ? null : value * 1e-6; })(),
    capacitanceF: solveFor === 'capacitance' ? null : equivalentCapacitance(bank, $('capacitor-connection').value),
    operatingFrequencyHz: numeric('operating-frequency', 'Switching frequency', { optional: true }) * scale[$('operating-frequency-unit').value] || null,
    seriesResistanceOhm: resistance,
    inductorTolerance: numeric('inductor-tolerance', 'Inductance tolerance', { zero: true, max: 99.99 }) / 100,
    capacitorTolerance: numeric('capacitor-tolerance', 'Capacitance tolerance', { zero: true, max: 99.99 }) / 100,
  };
  return { inputs, bank, leakageValue };
}

function renderResults(results, inputs, bank) {
  metric('result-frequency', results.resonantFrequencyHz, 'frequency');
  metric('result-inductance', inputs.solveFor === 'inductance' ? results.discreteInductanceH : results.totalInductanceH, 'inductance');
  setText('inductance-result-label', inputs.solveFor === 'inductance' ? 'Required discrete inductance · L' : 'Total series inductance · LΣ');
  metric('result-capacitance', results.capacitanceF, 'capacitance');
  const tolerance = results.tolerance;
  setText('frequency-range', tolerance ? `Corner range ${quantity(tolerance.frequencyMinHz, 'frequency')}–${quantity(tolerance.frequencyMaxHz, 'frequency')}` : 'Tolerance range unavailable');
  setText('inductance-breakdown', inputs.solveFor === 'inductance' ? `${quantity(results.totalInductanceH, 'inductance')} total including ${quantity(results.leakageInductanceH, 'inductance')} leakage` : `${quantity(results.discreteInductanceH, 'inductance')} discrete + ${quantity(results.leakageInductanceH, 'inductance')} leakage`);
  setText('capacitance-description', inputs.solveFor === 'capacitance' ? 'Required equivalent · bank not selected' : bank.length === 1 ? 'Entered equivalent · physical bank not inferred' : `${bank.length} entered values · ${$('capacitor-connection').value}`);
  setText('bank-note', inputs.solveFor === 'capacitance' ? 'The entered bank is a reference only; required equivalent C appears in the result.' : `Bank equivalent: ${quantity(results.capacitanceF, 'capacitance')}.`);
  setText('result-equation', inputs.solveFor === 'inductance' ? 'L = 1 / ((2πfᵣ)² Ceq) − Llk' : inputs.solveFor === 'capacitance' ? 'Ceq = 1 / ((2πfᵣ)² LΣ)' : 'fᵣ = 1 / (2π√(LΣ Ceq))');
  setText('result-substitution', `LΣ ${quantity(results.totalInductanceH, 'inductance')} · Ceq ${quantity(results.capacitanceF, 'capacitance')}`);
  setText('result-impedance', quantity(results.characteristicImpedanceOhm, 'resistance'));
  const hasOperatingPoint = Number.isFinite(inputs.operatingFrequencyHz) && inputs.operatingFrequencyHz > 0;
  setText('result-ratio', hasOperatingPoint ? `${number(results.frequencyRatio)} ×` : 'fₛ not provided');
  const region = !hasOperatingPoint ? 'fₛ not provided' : results.region ? String(results.region).replace(/^./, (c) => c.toUpperCase()) : (results.netReactanceOhm > 0 ? 'Inductive' : results.netReactanceOhm < 0 ? 'Capacitive' : 'Resonant');
  setText('result-region', region);
  setText('result-reactances', hasOperatingPoint ? `${quantity(results.inductiveReactanceOhm, 'resistance')} / ${quantity(results.capacitiveReactanceOhm, 'resistance')}` : 'fₛ not provided');
  setText('result-net-reactance', hasOperatingPoint ? `${results.netReactanceOhm > 0 ? '+' : ''}${quantity(results.netReactanceOhm, 'resistance')}` : 'fₛ not provided');
  setText('result-q', results.q === null || results.q === undefined ? 'R > 0 required' : `${number(results.q)} / ${quantity(results.bandwidthHz, 'frequency')}`);
  const selectedValue = inputs.solveFor === 'frequency' ? results.resonantFrequencyHz : inputs.solveFor === 'inductance' ? results.discreteInductanceH : results.capacitanceF;
  setText('selected-result-label', inputs.solveFor === 'frequency' ? 'Series resonance · fᵣ' : inputs.solveFor === 'inductance' ? 'Required discrete inductance · L' : 'Required equivalent capacitance · C');
  metric('selected-result-value', selectedValue, inputs.solveFor);
  setText('selected-result-note', inputs.solveFor === 'frequency' ? 'Ideal LC · nominal result' : 'Calculated requirement · part not selected');
  $('selected-result-strip').classList.remove('invalid');
}

function renderMagnetizing(branch) {
  const reference = transformerReference();
  setText('magnetizing-status', branch ? reference ? `${reference.label} · comparison` : 'Entered Lm · ideal branch' : 'Lm not provided');
  if (!branch) {
    ['magnetizing-open-frequency', 'magnetizing-reactance', 'magnetizing-ratio'].forEach((id) => setText(id, '—'));
    setText('magnetizing-note', 'Enter Lm or select an A/B reference to compare. The series result above works without it.');
    return;
  }
  metric('magnetizing-open-frequency', branch.openSecondaryFrequencyHz, 'frequency');
  metric('magnetizing-reactance', branch.magnetizingReactanceOhm, 'resistance');
  if (branch.magnetizingReactanceOhm === null) setText('magnetizing-reactance', 'fₛ not provided');
  setText('magnetizing-ratio', `${number(branch.inductanceRatio)} ×`);
  setText('magnetizing-note', 'Open-secondary estimate: f = 1 / (2π√((Lr + Lm)Ceq)). This assumes a linear primary-referred branch and a nonconducting rectifier. It is not the loaded operating frequency or converter gain; switching, pump dynamics and parasitics are omitted.');
}

function tableRow(values, classes = []) {
  const row = document.createElement('tr');
  values.forEach((value, index) => {
    const cell = document.createElement('td');
    cell.textContent = value;
    if (classes[index]) cell.className = classes[index];
    row.append(cell);
  });
  return row;
}

function renderCandidates() {
  const list = $('candidate-list');
  list.replaceChildren();
  if (!currentCalculation) { list.append(tableRow(['Enter valid circuit inputs.', '', '', ''])); return; }
  const { results } = currentCalculation;
  const type = $('candidate-type').value;
  const target = type === 'inductance' ? results.discreteInductanceH : results.capacitanceF;
  if (!Number.isFinite(target) || target <= 0) { list.append(tableRow(['Positive discrete L required for standard values.', '', '', ''])); return; }
  const candidates = preferredCandidates(target, $('preferred-series').value, 5);
  for (const candidate of candidates) {
    const frequency = type === 'inductance'
      ? resonanceFrequency(candidate.valueSI + results.leakageInductanceH, results.capacitanceF)
      : resonanceFrequency(results.totalInductanceH, candidate.valueSI);
    const difference = (frequency / results.resonantFrequencyHz - 1) * 100;
    const row = tableRow([
      quantity(candidate.valueSI, type),
      `${candidate.deviationPercent > 0 ? '+' : ''}${number(candidate.deviationPercent, 3)} %`,
      quantity(frequency, 'frequency'),
      `${difference > 0 ? '+' : ''}${number(difference, 3)} %`,
    ], ['number', 'number', 'number', 'number']);
    if (list.children.length === 0) row.className = 'nearest-value';
    list.append(row);
  }
}

function renderRecord({ inputs, results, bank, assumptions, magnetizingBranch, transformer }) {
  const basis = modified ? 'Edited input; preset is a reference' : 'Document preset; verify fitted hardware';
  recordRows = [
    ['Discrete series inductor', quantity(results.discreteInductanceH, 'inductance'), inputs.solveFor === 'inductance' ? 'Calculated requirement; part not selected' : basis],
    ['Transformer leakage', quantity(results.leakageInductanceH, 'inductance'), assumptions.leakageAssumedZero ? 'Not provided; assumed zero for calculation' : basis],
  ];
  if (bank) {
    const grouped = new Map();
    for (const value of bank) grouped.set(value, (grouped.get(value) || 0) + 1);
    for (const [value, count] of grouped) recordRows.push([bank.length === 1 ? 'Entered equivalent C' : `${count} × entered C value · ${$('capacitor-connection').value}`, quantity(value, 'capacitance'), inputs.solveFor === 'capacitance' ? 'Reference bank; excluded from C solution' : bank.length === 1 ? 'Single equivalent input; physical bank not inferred' : basis]);
  }
  recordRows.push([inputs.solveFor === 'capacitance' ? 'Required equivalent capacitor' : 'Bank equivalent capacitor', quantity(results.capacitanceF, 'capacitance'), inputs.solveFor === 'capacitance' ? 'Calculated requirement; physical bank not selected' : 'Calculated from entered bank']);
  recordRows.push(['Nominal resonance', quantity(results.resonantFrequencyHz, 'frequency'), 'Ideal LC equation']);
  if (inputs.operatingFrequencyHz) recordRows.push(['Switching frequency', quantity(inputs.operatingFrequencyHz, 'frequency'), basis]);
  recordRows.push(['Equivalent series resistance', inputs.seriesResistanceOhm === null ? 'Not provided' : quantity(inputs.seriesResistanceOhm, 'resistance'), inputs.seriesResistanceOhm > 0 ? 'User-entered series-RLC model input' : 'Q and bandwidth not calculated']);
  recordRows.push(['Total L / equivalent C range', `±${number(inputs.inductorTolerance * 100)} % / ±${number(inputs.capacitorTolerance * 100)} %`, 'Editable design ranges; not measured uncertainty']);
  recordRows.push(['Resonance corner interval', `${quantity(results.tolerance.frequencyMinHz, 'frequency')}–${quantity(results.tolerance.frequencyMaxHz, 'frequency')}`, 'Combined low/high L-total and C corners']);
  recordRows.push(['Transformer reference', transformer ? `${transformer.label} · supplied measurement` : 'Not identified / manual', 'Comparison only; installed identity unknown']);
  recordRows.push(['Magnetizing inductance · Lm', magnetizingBranch ? quantity(inputs.magnetizingInductanceH, 'inductance') : 'Not provided', 'Separate primary-referred shunt branch; excluded from series Lr']);
  if (transformer) recordRows.push(['Measured Np/Ns', number(transformer.turnsRatio), 'Reference only; reflected load and converter gain are not calculated']);
  if (magnetizingBranch) {
    recordRows.push(['Ideal open-secondary LC frequency', quantity(magnetizingBranch.openSecondaryFrequencyHz, 'frequency'), 'Linear, open-secondary limit; not a loaded converter prediction']);
    recordRows.push(['Magnetizing reactance at fs', quantity(magnetizingBranch.magnetizingReactanceOhm, 'resistance'), inputs.operatingFrequencyHz ? 'Xm = 2 pi fs Lm; not inferred branch current' : 'Operating frequency not provided']);
    recordRows.push(['Lm / Lr', number(magnetizingBranch.inductanceRatio), 'Ratio to external plus primary-referred leakage inductance']);
  }
  const list = $('bom-list');
  list.replaceChildren(...recordRows.map((row) => tableRow(row)));
}

function calculate() {
  clearValidation(form);
  const solveFor = updateSolveControls();
  const operatingRaw = $('operating-frequency').value.trim();
  const resistanceRaw = $('series-resistance').value.trim();
  setText('advanced-inputs-summary', `fₛ ${operatingRaw || '—'} ${$('operating-frequency-unit').value} · R ${resistanceRaw ? `${resistanceRaw} Ω` : 'not set'} · L ±${$('inductor-tolerance').value || '—'}% / C ±${$('capacitor-tolerance').value || '—'}%`);
  renderSource();
  const leakageBlank = $('leakage-inductance').value.trim() === '';
  setText('leakage-note', leakageBlank ? 'Leakage not provided; 0 µH is a calculation assumption. Add a measured or documented value.' : 'Included in total series L. Use leakage referred to the same transformer side as the discrete inductor.');
  $('leakage-note').classList.toggle('known', !leakageBlank);
  try {
    const { inputs, bank, leakageValue } = readInputs(solveFor);
    const results = analyzeTank(inputs);
    const magnetizingBranch = inputs.magnetizingInductanceH === null ? null : analyzeMagnetizingBranch({
      totalInductanceH: results.totalInductanceH, capacitanceF: results.capacitanceF,
      magnetizingInductanceH: inputs.magnetizingInductanceH, operatingFrequencyHz: inputs.operatingFrequencyHz,
    });
    const assumptions = {
      leakageAssumedZero: leakageValue === null,
      model: 'Ideal LC resonance / ideal series RLC; not a full converter model',
      tolerance: 'Independent low/high L-total and C corners; no measured component distribution',
      capacitorSolutionIsEquivalentOnly: solveFor === 'capacitance',
      inputsModifiedFromPreset: modified,
      magnetizingBranch: inputs.magnetizingInductanceH === null ? 'Lm unknown; no branch estimates' : 'Linear primary-referred Lm; open-secondary LC estimate excludes load, rectifier conduction, switching, pump and parasitics',
      transformerIdentity: 'A/B references are comparisons; installed identity is not recorded',
    };
    currentCalculation = { inputs, results, bank, assumptions, magnetizingBranch, transformer: transformerReference() };
    $('calculation-error').hidden = true;
    renderResults(results, inputs, bank);
    renderMagnetizing(magnetizingBranch);
    renderRecord(currentCalculation);
    const warnings = [...(selectedPreset?.warnings || []), ...(results.warnings || [])];
    if (leakageValue === null) warnings.push('Transformer leakage is not provided. The displayed result uses 0 µH; it is an assumption, not a measured value.');
    if (modified) warnings.push('Inputs differ from the source preset. The cited document is a baseline, not evidence of the edited values.');
    if (inputs.solveFor === 'capacitance') warnings.push('The calculated C is an equivalent requirement. It does not establish a capacitor count, voltage rating, ripple-current rating, or a safe component selection.');
    warnings.push('The series-response plot excludes the magnetizing branch. Separate Lm estimates assume an ideal open secondary, not a loaded converter. Rectification, charge-pump switching and parasitics are not modeled; fₛ above fᵣ alone does not establish ZVS.');
    warningsList(warnings);
    ['copy-bom', 'export-csv', 'export-json'].forEach((id) => { $(id).disabled = false; });
  } catch (error) {
    currentCalculation = null;
    recordRows = [];
    renderMagnetizing(null);
    setText('magnetizing-status', 'Check circuit inputs');
    setText('calculation-error', error.message || 'Check the circuit inputs.');
    $('calculation-error').hidden = false;
    ['result-frequency', 'result-inductance', 'result-capacitance', 'result-impedance', 'result-ratio', 'result-region', 'result-reactances', 'result-net-reactance', 'result-q'].forEach((id) => setText(id, '—'));
    setText('frequency-range', 'No valid result');
    setText('inductance-breakdown', 'Check circuit inputs');
    setText('capacitance-description', 'Check circuit inputs');
    setText('result-substitution', '');
    setText('selected-result-label', 'Calculation incomplete');
    setText('selected-result-value', 'Input required');
    setText('selected-result-note', 'Check the marked fields below.');
    $('selected-result-strip').classList.add('invalid');
    if (!form.querySelector('[aria-invalid="true"]')) {
      const field = solveFor === 'frequency' ? 'discrete-inductance' : 'target-frequency';
      markFieldInvalid(field, error.message || 'Check this value and the other circuit inputs.');
    }
    $('bom-list').replaceChildren(tableRow(['No valid calculation.', '—', 'Correct the inputs before exporting.']));
    warningsList(selectedPreset?.warnings || []);
    ['copy-bom', 'export-csv', 'export-json'].forEach((id) => { $(id).disabled = true; });
  }
  renderCandidates();
  drawResponse();
}

function applyPreset(id) {
  selectedPreset = PRESETS.find((preset) => preset.id === id) || PRESETS[0];
  if (!selectedPreset) throw new Error('No circuit presets are available.');
  $('tank-preset').value = selectedPreset.id;
  const reference = TRANSFORMER_REFERENCES.find((item) => item.id === selectedPreset.transformerReferenceId);
  $('transformer-reference').value = reference?.id || 'custom';
  $('magnetizing-inductance').value = reference?.magnetizingInductanceUh ?? '';
  $('discrete-inductance').value = selectedPreset.discreteInductanceUh ?? '';
  $('leakage-inductance').value = selectedPreset.leakageInductanceUh ?? '';
  $('capacitor-values').value = (selectedPreset.capacitorsNf || []).join(', ');
  $('capacitor-unit').value = 'nF';
  $('capacitor-connection').value = selectedPreset.capacitorConnection || 'parallel';
  $('target-frequency').value = selectedPreset.targetFrequencyKhz ?? selectedPreset.operatingFrequencyKhz ?? 120;
  $('target-frequency-unit').value = 'kHz';
  $('operating-frequency').value = selectedPreset.operatingFrequencyKhz ?? '';
  $('operating-frequency-unit').value = 'kHz';
  $('series-resistance').value = selectedPreset.seriesResistanceOhm ?? '';
  $('inductor-tolerance').value = selectedPreset.inductorTolerancePercent ?? 10;
  $('capacitor-tolerance').value = selectedPreset.capacitorTolerancePercent ?? 5;
  modified = false;
  setText('export-status', 'Export includes the inputs, source references, assumptions, and calculation results.');
  calculate();
}

function drawResponse() {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  if (!width || !height) return;
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(width * ratio);
  canvas.height = Math.round(height * ratio);
  ctx.scale(ratio, ratio);
  ctx.clearRect(0, 0, width, height);
  ctx.font = '10px Consolas, monospace';
  if (!currentCalculation) {
    ctx.fillStyle = '#8297a5';
    ctx.textAlign = 'center';
    ctx.fillText('Enter valid inputs to display the calculated response.', width / 2, height / 2);
    canvas.setAttribute('aria-label', 'No response: circuit inputs are invalid.');
    return;
  }
  const { inputs, results } = currentCalculation;
  const R = inputs.seriesResistanceOhm;
  const normalized = R > 0;
  setText('plot-legend', normalized ? 'Normalized series current · I / Iᵣ' : 'Net series reactance · Ω');
  setText('response-note', normalized ? `Ideal series RLC · R = ${quantity(R, 'resistance')} · current at constant drive voltage` : 'R not provided or zero: reactance shown; Q and bandwidth require R > 0.');
  const margins = { left: 54, right: 14, top: 17, bottom: 34 };
  const plotWidth = width - margins.left - margins.right;
  const plotHeight = height - margins.top - margins.bottom;
  const x = (frequencyRatio) => margins.left + (Math.log(frequencyRatio / 0.25) / Math.log(16)) * plotWidth;
  const reactance = (frequencyRatio) => results.characteristicImpedanceOhm * (frequencyRatio - 1 / frequencyRatio);
  const maxX = Math.max(Math.abs(reactance(0.25)), Math.abs(reactance(4))) * 1.05;
  const yMin = normalized ? 0 : -maxX;
  const yMax = normalized ? 1.08 : maxX;
  const y = (value) => margins.top + (1 - (value - yMin) / (yMax - yMin)) * plotHeight;
  ctx.lineWidth = 1;
  ctx.strokeStyle = '#29363f';
  ctx.fillStyle = '#8194a1';
  ctx.textAlign = 'right';
  for (let i = 0; i <= 4; i++) {
    const value = normalized ? i / 4 : -maxX + (i / 4) * 2 * maxX;
    const ypos = y(value);
    ctx.beginPath(); ctx.moveTo(margins.left, ypos); ctx.lineTo(width - margins.right, ypos); ctx.stroke();
    ctx.fillText(number(value, 3), margins.left - 9, ypos + 3);
  }
  ctx.textAlign = 'center';
  for (const tick of [0.25, 0.5, 1, 2, 4]) {
    const xpos = x(tick);
    ctx.strokeStyle = tick === 1 ? '#4b5e69' : '#29363f';
    ctx.setLineDash(tick === 1 ? [3, 4] : []);
    ctx.beginPath(); ctx.moveTo(xpos, margins.top); ctx.lineTo(xpos, height - margins.bottom); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = tick === 1 ? '#c3cfd7' : '#8194a1';
    ctx.textAlign = tick === 0.25 ? 'left' : tick === 4 ? 'right' : 'center';
    ctx.fillText(quantity(tick * results.resonantFrequencyHz, 'frequency', 3), xpos, height - 17);
  }
  const drawRatios = Array.from({ length: 321 }, (_, i) => 0.25 * 16 ** (i / 320));
  drawRatios.push(1);
  drawRatios.sort((a, b) => a - b);
  ctx.lineWidth = 1.7;
  ctx.strokeStyle = '#f0d365';
  ctx.beginPath();
  drawRatios.forEach((frequencyRatio, index) => {
    const net = reactance(frequencyRatio);
    const value = normalized ? R / Math.hypot(R, net) : net;
    if (index === 0) ctx.moveTo(x(frequencyRatio), y(value)); else ctx.lineTo(x(frequencyRatio), y(value));
  });
  ctx.stroke();
  if (Number.isFinite(inputs.operatingFrequencyHz) && Number.isFinite(results.frequencyRatio)) {
    const fsRatio = results.frequencyRatio;
    if (fsRatio >= 0.25 && fsRatio <= 4) {
      const net = reactance(fsRatio);
      const value = normalized ? R / Math.hypot(R, net) : net;
      ctx.strokeStyle = '#67cbd1'; ctx.lineWidth = 1; ctx.setLineDash([3, 4]);
      ctx.beginPath(); ctx.moveTo(x(fsRatio), margins.top); ctx.lineTo(x(fsRatio), height - margins.bottom); ctx.stroke();
      ctx.setLineDash([]); ctx.fillStyle = '#67cbd1';
      ctx.beginPath(); ctx.arc(x(fsRatio), y(value), 3.5, 0, 2 * Math.PI); ctx.fill();
      ctx.textAlign = fsRatio > 2.8 ? 'right' : 'left';
      ctx.fillText('fₛ', x(fsRatio) + (fsRatio > 2.8 ? -6 : 6), margins.top + 9);
    } else {
      ctx.textAlign = 'right'; ctx.fillStyle = '#67cbd1';
      ctx.fillText('fₛ outside plotted range', width - margins.right, margins.top + 9);
    }
  }
  canvas.setAttribute('aria-label', normalized ? `Calculated ideal normalized series-RLC current; resonance at ${quantity(results.resonantFrequencyHz, 'frequency')}, series resistance ${quantity(R, 'resistance')}. Not measured converter gain.` : `Calculated net series reactance, crossing zero at ${quantity(results.resonantFrequencyHz, 'frequency')}. Resistance not provided; no current-response or converter-gain prediction.`);
}

function exportObject() {
  if (!currentCalculation) return null;
  return {
    schema: 'thesis-power-lab-resonance-v1',
    createdAt: new Date().toISOString(),
    preset: { id: selectedPreset.id, label: selectedPreset.label, sourceNote: selectedPreset.sourceNote, sourceIds: sourceIds() },
    sourceReferences: Object.fromEntries(sourceIds().map((id) => [id, SOURCES[id] || { title: id }])),
    inputUnits: 'SI: H, F, Hz, ohm; fractional tolerances',
    inputs: currentCalculation.inputs,
    magnetizingBranch: currentCalculation.magnetizingBranch,
    transformerReference: currentCalculation.transformer, 
    enteredCapacitorBank: { valuesF: currentCalculation.bank, connection: $('capacitor-connection').value, usedInSolution: currentCalculation.inputs.solveFor !== 'capacitance' },
    assumptions: currentCalculation.assumptions,
    results: { ...currentCalculation.results, ...(!currentCalculation.inputs.operatingFrequencyHz ? { operatingFrequencyHz: null, inductiveReactanceOhm: null, capacitiveReactanceOhm: null, netReactanceOhm: null, frequencyRatio: null, region: null } : {}) },
    warnings: [...$('calculation-warnings').children].map((item) => item.textContent),
    record: recordRows.map(([item, value, basis]) => ({ item, value, basis })),
    comparison: { component: $('candidate-type').value, preferredSeries: $('preferred-series').value, partsSelected: false },
  };
}

function download(content, mime, extension, prefix = `tank-${selectedPreset.id}`) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = `${prefix}-${new Date().toISOString().slice(0, 10)}.${extension}`;
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function csvCell(value) { return `"${String(value ?? '').replaceAll('"', '""')}"`; }

function calculatePump() {
  clearValidation($('pump-form'));
  const solveFor = $('pump-solve-for').value;
  $('pump-inductance').disabled = solveFor === 'inductance';
  $('pump-capacitance').disabled = solveFor === 'capacitance';
  $('pump-frequency').disabled = solveFor === 'frequency';
  $('pump-frequency-unit').disabled = solveFor === 'frequency';
  setText('pump-result-label', solveFor === 'inductance' ? 'Estimated pump inductance · Lp' : solveFor === 'capacitance' ? 'Estimated pump capacitance · Cp' : 'Estimated switching carrier · fₛ');
  setText('pump-equation', solveFor === 'inductance' ? 'Lp = 1 / (16 Cp fₛ²)' : solveFor === 'capacitance' ? 'Cp = 1 / (16 Lp fₛ²)' : 'fₛ = 1 / (4√(Lp Cp))');
  try {
    const inputs = {
      solveFor,
      inductanceH: solveFor === 'inductance' ? null : numeric('pump-inductance', 'Pump inductance') * 1e-6,
      capacitanceF: solveFor === 'capacitance' ? null : numeric('pump-capacitance', 'Pump capacitance') * 1e-9,
      switchingFrequencyHz: solveFor === 'frequency' ? null : numeric('pump-frequency', 'Pump switching carrier') * scale[$('pump-frequency-unit').value],
    };
    const results = analyzePump(inputs);
    currentPumpCalculation = { inputs, results };
    const value = solveFor === 'inductance' ? results.inductanceH : solveFor === 'capacitance' ? results.capacitanceF : results.switchingFrequencyHz;
    metric('pump-result-value', value, solveFor);
    metric('pump-natural-frequency', results.pumpResonantFrequencyHz, 'frequency');
    $('pump-error').hidden = true;
    $('export-pump').disabled = false;
  } catch (error) {
    currentPumpCalculation = null;
    setText('pump-result-value', '—');
    setText('pump-natural-frequency', '—');
    setText('pump-error', error.message || 'Check the pump sizing inputs.');
    $('pump-error').hidden = false;
    $('export-pump').disabled = true;
  }
}

for (const id of ['target-frequency', 'discrete-inductance', 'leakage-inductance', 'magnetizing-inductance', 'capacitor-values', 'operating-frequency', 'series-resistance', 'inductor-tolerance', 'capacitor-tolerance', 'pump-inductance', 'pump-capacitance', 'pump-frequency']) {
  const input = $(id);
  const feedback = document.createElement('span');
  feedback.id = `validation-${id}`;
  feedback.className = 'field-error';
  feedback.hidden = true;
  const anchor = input.closest('.calc-input-row') || input.closest('.bank-row') || input.closest('.value-with-unit') || input;
  anchor.after(feedback);
  const descriptions = new Set((input.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean));
  descriptions.add(feedback.id);
  input.setAttribute('aria-describedby', [...descriptions].join(' '));
}

const presetDisplayLabels = {
  'thesis-tested-nominal': 'Tested V1.0 · thesis LC',
  'thesis-transformer-a': 'Transformer A · thesis LC',
  'f410-drawing-values': 'F410 drawing · C26 missing',
  'f410-thesis-scenario': 'F410 + thesis assumptions',
  'v11-drawing-values': 'V1.1 drawing · C26 missing',
};
$('tank-preset').replaceChildren(...PRESETS.map((preset) => {
  const option = document.createElement('option');
  option.value = preset.id;
  option.textContent = presetDisplayLabels[preset.id] || preset.label;
  option.title = preset.label;
  return option;
}));
form.addEventListener('submit', (event) => event.preventDefault());
form.addEventListener('input', (event) => {
  if (event.target.id === 'tank-preset' || event.target.id === 'transformer-reference') return;
  if (['magnetizing-inductance', 'leakage-inductance'].includes(event.target.id)) $('transformer-reference').value = 'custom';
  if (event.target.id !== 'solve-for') modified = true;
  if (event.target.id === 'solve-for' && event.target.value !== 'frequency') $('candidate-type').value = event.target.value;
  calculate();
});
$('transformer-reference').addEventListener('change', () => {
  const reference = transformerReference();
  if (reference) {
    $('leakage-inductance').value = reference.leakageInductanceUh;
    $('magnetizing-inductance').value = reference.magnetizingInductanceUh;
  }
  modified = true;
  calculate();
});
$('tank-preset').addEventListener('change', () => applyPreset($('tank-preset').value));
$('reset-preset').addEventListener('click', () => applyPreset($('tank-preset').value));
$('candidate-type').addEventListener('change', renderCandidates);
$('preferred-series').addEventListener('change', renderCandidates);
$('export-json').addEventListener('click', () => {
  const data = exportObject();
  if (!data) return;
  download(`${JSON.stringify(data, null, 2)}\n`, 'application/json', 'json');
  setText('export-status', 'JSON exported with SI inputs, results, assumptions, and source references.');
});
$('export-csv').addEventListener('click', () => {
  const data = exportObject();
  if (!data) return;
  const rows = [['Item', 'Value', 'Basis'], ...recordRows, [], ['Preset', selectedPreset.label, modified ? 'Modified inputs' : 'Document values'], ['Created', data.createdAt, 'UTC'], ...data.warnings.map((warning) => ['Model note', warning, '']), ...Object.entries(data.sourceReferences).map(([id, source]) => ['Source', source.title, `${id}: ${source.detail || ''}`])];
  download(`\uFEFF${rows.map((row) => row.map(csvCell).join(',')).join('\r\n')}\r\n`, 'text/csv;charset=utf-8', 'csv');
  setText('export-status', 'Calculation table and source/model notes exported as CSV.');
});
$('copy-bom').addEventListener('click', async () => {
  if (!currentCalculation) return;
  const table = [['Item', 'Value', 'Basis'], ...recordRows].map((row) => row.join('\t')).join('\n');
  try {
    await navigator.clipboard.writeText(table);
    setText('export-status', 'Calculation table copied. Paste it into your notes or a spreadsheet.');
  } catch {
    setText('export-status', 'Clipboard access is unavailable. Export CSV to copy the calculation table.');
  }
});
$('pump-form').addEventListener('submit', (event) => event.preventDefault());
$('pump-form').addEventListener('input', calculatePump);
$('export-pump').addEventListener('click', () => {
  if (!currentPumpCalculation) return;
  const data = {
    schema: 'thesis-power-lab-pump-v1',
    createdAt: new Date().toISOString(),
    model: 'Thesis clamped triangular-current charge-pump approximation',
    source: 'Chapter 4, Pump Inductor Design; 05_Pump_Inductor.tex',
    equations: ['Lp = 1 / (16 Cp fs^2)', 'fp = 1 / (2 pi sqrt(Lp Cp)) = 2 fs / pi'],
    inputUnits: 'SI: H, F, Hz',
    ...currentPumpCalculation,
    assumptions: ['Equivalent Cp is separate from the resonant-tank capacitor.', 'Approximate triangular-current and clamped-cycle model.', 'Clamp timing, current, temperature, and device ratings are not verified.'],
  };
  download(`${JSON.stringify(data, null, 2)}\n`, 'application/json', 'json', 'charge-pump-sizing');
  setText('pump-export-status', 'Pump sizing exported with SI inputs, results, source, and model assumptions.');
});
if (typeof ResizeObserver !== 'undefined') new ResizeObserver(drawResponse).observe(canvas.parentElement);
window.addEventListener('resize', drawResponse);
applyPreset(PRESETS[0]?.id);
calculatePump();
