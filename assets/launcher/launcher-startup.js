"use strict";
/* Installed before UI scripts so a missing/broken script cannot leave an unreported blank page. */
(() => {
  let finished = false;
  function signal(status, reason) {
    if (typeof AndroidLauncher !== "undefined" && typeof AndroidLauncher.startup === "function")
      AndroidLauncher.startup(status, String(reason || "").slice(0, 200));
  }
  function fail(reason) {
    if (finished) return;
    finished = true; signal("failed", reason);
  }
  window.addEventListener("error", event => {
    const target = event.target;
    if (target && target !== window && !["SCRIPT", "LINK"].includes(target.tagName)) return;
    fail(event.message || "Required UI resource failed");
  }, true);
  window.addEventListener("unhandledrejection", event => fail(event.reason && event.reason.message || "UI initialization rejected"));
  window.LauncherStartup = {
    fail,
    ready() {
      if (finished) return;
      const ui = window.EditorUI;
      if (!window.Launcher || !window.LauncherApi || !window.EditorCore || !ui ||
          !ui.U || !ui.W || !ui.Store || !ui.compare || typeof ui.enter !== "function" || typeof ui.back !== "function") {
        fail("Player editor modules are incomplete"); return;
      }
      finished = true; signal("ready", "");
    }
  };
})();
