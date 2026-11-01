"use strict";
/* Pure player-editor rules, ported 1:1 from EditorForm.java and EditorSearch.java.
   No DOM access, so it runs in the page and under node (see preview/test-editor-core.js). */
(function (root) {
  const fail = m => { throw new RangeError(m); };

  const careerCost = n => {
    if (!Number.isInteger(n) || n < 0 || n > 1000) fail("Training count is out of range");
    const q = Math.floor(n / 4), r = n % 4;
    return 2 * q * (q + 1) + r * (q + 1);
  };
  const allocationTarget = (current, requested, balance) => {
    if (current < 0 || current > 1000 || balance < 0) fail("Invalid training draft format");
    let target = Math.max(0, Math.min(1000, requested));
    if (target <= current) return target;
    const total = careerCost(current) + balance;
    while (target > current && careerCost(target) > total) target--;
    return target;
  };
  const allocationMaximum = (current, totalBudget, capacity) => {
    if (current < 0 || current > 1000 || totalBudget < 0 || capacity < 0) fail("Invalid training scale format");
    let max = 0; const limit = Math.min(1000, capacity);
    while (max < limit && careerCost(max + 1) <= totalBudget) max++;
    return Math.max(current, max);
  };
  const remaining = (budget, initialLevel, level, limit, counts) => {
    if (budget < 0 || initialLevel < 1 || level < initialLevel || level > limit || limit > 1000 || counts.length !== 10) fail("Invalid training draft format");
    let balance = budget + 2 * (level - initialLevel);
    for (const c of counts) balance -= careerCost(c);
    return balance;
  };
  const nextLevel = (level, limit) => {
    if (level < 1 || level > limit || limit > 1000) fail("Invalid level format");
    return Math.min(limit, level + 1);
  };
  const DEFAULT_LEVEL_CAP = 50;
  const levelLimit = (raw, currentLevel, levelCap = DEFAULT_LEVEL_CAP, existingLimit = currentLevel) => {
    const s = String(raw).trim();
    if (!/^[0-9]{1,4}$/.test(s)) fail("Enter an integer for the level limit");
    const value = parseInt(s, 10);
    if (levelCap < 1 || currentLevel < 1 || existingLimit < currentLevel) fail("Invalid level-limit type");
    const max = Math.max(levelCap, existingLimit);
    if (value < currentLevel || value > max) fail(`Level limit range: ${currentLevel}～${max}`);
    if (value > levelCap && value !== existingLimit) fail(`Original limit %d preserved${levelCap} levels`);
    return value;
  };
  const developmentAbility = (base, saved, increments) => {
    if (base < 0 || base > 127 || saved < 0 || saved > 127 || increments < 0) fail("Invalid training ability format");
    return Math.min(Math.max(105, Math.max(base, saved)), base + increments);
  };
  const abilityBand = v => (v < 70 ? "b0" : v < 80 ? "b1" : v < 90 ? "b2" : v < 100 ? "b3" : "b4");
  const aptitudeIndexForPosition = p => {
    if (!Number.isInteger(p) || p < 0 || p > 12) fail("Main position is out of range.");
    return [12, 9, 10, 11, 5, 6, 7, 8, 4, 2, 3, 1, 0][p];
  };
  const nextAptitude = (state, isMain) => {
    if (state < 0 || state > 2) fail("Proficiency is out of range.");
    return isMain ? 2 : (state + 1) % 3;
  };
  const skills = (choices, ids) => {
    if (choices.length > 10) fail("A maximum of 10 additional skills is allowed.");
    const out = [];
    for (const c of choices) {
      if (c === 0) continue;
      if (c < 0 || c > ids.length) fail("Skill selection changed");
      const id = ids[c - 1];
      if (out.includes(id)) fail("Duplicate additional skill; choose a different skill for each slot");
      out.push(id);
    }
    return out;
  };

  // EditorSearch
  const matches = (query, searchable, scope, current, inSquad, warehouse) => {
    if ((scope === 1 && !current) || (scope === 2 && !inSquad) || (scope === 3 && !warehouse) || (scope === 4 && (inSquad || warehouse))) return false;
    const hay = String(searchable).toLowerCase(), q = String(query).trim().toLowerCase();
    if (!q) return true;
    return q.split(/\s+/).every(t => hay.includes(t));
  };
  const catalogMatches = (query, searchable, selectedPosition, position, selectedType, type) => {
    if (selectedPosition >= 0 && selectedPosition !== position) return false;
    if (selectedType && selectedType !== type) return false;
    return matches(query, searchable, 0, false, false, false);
  };

  const api = {careerCost, allocationTarget, allocationMaximum, remaining, nextLevel, levelLimit, developmentAbility, abilityBand,
    aptitudeIndexForPosition, nextAptitude, skills, matches, catalogMatches, DEFAULT_LEVEL_CAP};
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.EditorCore = api;
})(typeof window !== "undefined" ? window : globalThis);
