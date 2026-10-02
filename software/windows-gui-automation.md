# Windows GUI automation

Start from the accessibility tree, not pixels. Microsoft UI Automation (UIA) exposes windows and controls as a live tree of properties and patterns ([overview](https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-treeoverview)). Every UIA tool can automate only what the app exposes. For an owned app with opaque custom controls, add UIA providers or automation peers rather than image recognition.

## Tool choice (July 2026)

| Need | Use |
|---|---|
| Agent exploration, shell scripts, smoke tests, bounded production flows | **[WinApp CLI](https://github.com/microsoft/winappCli/blob/c0578fcf5a2a1e3e7e5002e4521c446fb549365f/docs/ui-automation.md)**: inspect and search the tree as JSON, screenshot, invoke, set and read values, wait with exit codes, real-input fallback. Young (0.5.0); verify on the real app. |
| Code-first .NET test suite | **FlaUI**: UIA2 and UIA3 wrappers. UIA2 still helps with some WinForms quirks. |
| Python, mixed Win32 and UIA | **pywinauto**: separate backends and input fallback. Its UIA backend can't see custom properties. |
| No-code record-and-replay, business RPA | **Power Automate Desktop**: recorder plus selector repository (UIA, MSAA, text, image). |
| Existing Appium contract only | **Appium Windows Driver**: proxies the unmaintained WinAppDriver. Never use it for new work. |

WinApp CLI is a driver, not a workflow engine. The caller owns business state, idempotency, persisted progress, retries, restarts, compound readiness checks, and result classification. Use a library or hybrid when you need raw Win32 messages, image interpretation, or fine focus and timing control. Add a driver abstraction only once a second driver covers a real workflow end to end.

## Capturing state

Windows has no HAR equivalent. At each meaningful state, keep a UIA JSON dump, a screenshot, and an action log entry (action, selector, expected state). Keep app version and PID or HWND when they disambiguate, and DPI and coordinates only when physical input was used.

```powershell
winapp ui inspect -a $appPid --depth 8 --json | Set-Content -Encoding utf8 "$state.uia.json"
winapp ui screenshot -a $appPid --output "$state.png"   # --capture-screen for menus and overlays
```

Re-capture after every menu, dialog, or tab, because one dump never covers later surfaces. Selectors: prefer `AutomationId` plus control type. Names may be localized, generated slugs and runtime IDs are snapshot-local, and coordinates are a last resort.

Image matching, OCR, shortcuts, and coordinate input are fallbacks for opaque regions only. They break on layout, scaling, focus, theme, and locale, so confirm each effect with another capture. Physical input needs an unlocked desktop and matching privilege; UAC, elevation mismatch, and RDP state can block it ([UIPI](https://learn.microsoft.com/en-us/troubleshoot/power-platform/power-automate/desktop-flows/ui-automation/uipi-issues)).

## Keeping the desktop alive after RDP

Closing an RDP client locks the session. Instead, move the session to the console with `tscon`: the desktop stays unlocked and processes keep running. Reconnecting via RDP pulls it back, so repeat the move after every maintenance connection.

Verified on one host: `tscon` returned error 5 for an unelevated standard user, and also for a *separate* elevated admin. What worked was making the interactive user a local admin, signing out and back in for a new token, then elevating PowerShell as that same user (`whoami` confirms it).

```powershell
Add-LocalGroupMember -Group (Get-LocalGroup -SID 'S-1-5-32-544') -Member 'CONTOSO\automation'   # one-time
tscon.exe (Get-Process -Id $PID).SessionId /dest:console
```

For a reusable shortcut, set the target to `powershell.exe -NoProfile -WindowStyle Hidden -Command "$id=(Get-Process -Id $PID).SessionId; tscon.exe $id /dest:console"` and tick Advanced → Run as administrator. UAC approval is still required. ([tscon](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tscon))
