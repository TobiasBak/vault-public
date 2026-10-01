# Windows GUI automation

Start Windows GUI automation with the accessibility model, not pixels. Microsoft UI Automation (UIA) exposes windows and controls as a tree with properties and interaction patterns. Elements appear, move, and disappear as the interface changes. The tree describes live state, not a recorded interaction log like a browser HAR. [Microsoft's UIA tree overview](https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-treeoverview)

## Default choice

As of July 2026, **WinApp CLI is the default for agent or shell-driven discovery and control**. Use the table below for other needs.

WinApp CLI packages the useful primitives into small commands: inspect or search the UIA tree, emit JSON, capture a screenshot, invoke controls, set and read values, wait for state, and fall back to real input for operations that UIA patterns cannot express. It works across Win32, WinForms, WPF, WinUI, and Electron to the extent that those applications expose UIA. Its `AutomationId` selectors are preferable when unique; generated slugs can become stale after the UI changes. [WinApp CLI UIA and input model](https://github.com/microsoft/winappCli/blob/c0578fcf5a2a1e3e7e5002e4521c446fb549365f/docs/ui-automation.md#L6-L15), [selector behavior](https://github.com/microsoft/winappCli/blob/c0578fcf5a2a1e3e7e5002e4521c446fb549365f/docs/ui-automation.md#L67-L83), [JSON tree output](https://github.com/microsoft/winappCli/blob/c0578fcf5a2a1e3e7e5002e4521c446fb549365f/docs/ui-automation.md#L668-L687)

This recommendation rests on interface fit, not a benchmark: stateless commands, machine-readable output, screenshots, and waits with meaningful exit codes. At the reviewed `0.5.0` release, the tool was young. Verify the real application before relying on it for consequential work. [WinApp CLI 0.5.0 version](https://github.com/microsoft/winappCli/blob/fd7cb6f235fa54dd2c6e26386e65e967a2c8797a/version.json#L1-L3)

## Driver, not workflow architecture

WinApp CLI supports automation and CI, not just debugging. It can drive bounded production flows with reliable UIA controls: find a target, act, read a value, wait, or capture evidence. The caller owns the workflow. [WinApp CLI CI and assertion examples](https://github.com/microsoft/winappCli/blob/c0578fcf5a2a1e3e7e5002e4521c446fb549365f/docs/ui-automation.md#L620-L665)

Keep these concerns in application code or an automation platform:

- business state and state transitions;
- idempotency and persisted progress;
- retries, process restart, compensation, and safe termination;
- readiness conditions that combine UIA, native windows, process state, or image evidence;
- domain-specific result classification, observability, and operator handoff.

Use a direct library or hybrid when the CLI cannot express needed Win32 messages, image interpretation, or focus and timing control. Existing production automation can keep its workflow and interaction code while using WinApp CLI for discovery, capture, diagnostics, and smoke checks.

Add an interchangeable driver interface only when a second driver covers a real workflow end to end. Otherwise it adds indirection without containing application-specific exceptions.

Choose by use case:

| Need | Default | Why |
|---|---|---|
| Agent exploration, bounded production automation, shell scripts, or smoke tests | **WinApp CLI** | The shortest path from tree inspection and screenshot to interaction and assertion. |
| A maintained, code-first .NET UI test suite | **FlaUI** | A broad .NET wrapper over UIA2 and UIA3 that also exposes native UIA objects when its abstraction is insufficient. UIA2 can still help with some WinForms cases where UIA3 is troublesome. [FlaUI scope](https://github.com/FlaUI/FlaUI/blob/5e364212d4c7f37c68a8ca1016064be37926fb87/README.md#L13-L16), [UIA2/UIA3 tradeoff](https://github.com/FlaUI/FlaUI/blob/5e364212d4c7f37c68a8ca1016064be37926fb87/README.md#L22-L34) |
| Python automation, especially when both legacy Win32 and UIA backends matter | **pywinauto** | It exposes separate Win32 and UIA backends and can fall back to mouse and keyboard events when controls are not visible to inspection tools. Its UIA backend does not expose custom properties and controls because of its `comtypes` boundary. [pywinauto backends and limits](https://github.com/pywinauto/pywinauto/blob/18d2a95cebed2f0061ab4e4c80c3a76ece5dd4f3/docs/getting_started.txt#L5-L21), [input fallback](https://github.com/pywinauto/pywinauto/blob/18d2a95cebed2f0061ab4e4c80c3a76ece5dd4f3/docs/getting_started.txt#L58-L63) |
| No-code recording, business RPA, and a managed selector repository | **Power Automate Desktop** | Its recorder creates actions and captured elements. Its picker can use UIA, UIA3 Raw, or MSAA, and it also supports text-based selectors and image-based recording. [UI element selectors](https://learn.microsoft.com/en-us/power-automate/desktop-flows/ui-elements), [desktop recorder](https://learn.microsoft.com/en-us/power-automate/desktop-flows/recording-flow) |
| An existing Appium/WebDriver contract that cannot reasonably be replaced | **Appium Windows Driver** | Keep it for ecosystem compatibility, not as the default for new work. The Appium driver is a proxy around Microsoft's closed-source WinAppDriver server, and its own maintainers explicitly warn that Microsoft has not maintained that server for years. [Appium warning and prerequisites](https://github.com/appium/appium-windows-driver/blob/a3f2f04b3d888dbc1244af533afadb93e71db18d/README.md#L9-L30), [backend limitation](https://github.com/appium/appium-windows-driver/blob/a3f2f04b3d888dbc1244af533afadb93e71db18d/README.md#L407-L417) |

Power Automate Desktop's recorded flow is the closest option when the requirement is literal record-and-replay. It is a tool-specific executable workflow, not a portable Windows equivalent of HAR. WinApp CLI is a better handoff format for an agent because the artifacts remain ordinary JSON, PNG, and text.

## A HAR-like capture bundle

Windows has no standard GUI artifact combining HAR's recording, interchange, and replay. Capture a **UIA JSON tree and screenshot at each meaningful state**, plus a short action log.

For each step, retain:

- the action and selector used;
- expected state or assertion;
- `winapp ui inspect --json` output;
- a normal window screenshot, or `--capture-screen` when menus, flyouts, or overlays matter;
- target application version and PID or HWND when they help reproduce ambiguity;
- display scaling and coordinates only for steps forced to use physical input.

Example capture:

```powershell
$appPid = 12345
$state = "01-main-window"

winapp ui inspect -a $appPid --depth 8 --json |
  Set-Content -Encoding utf8 "$state.uia.json"
winapp ui screenshot -a $appPid --output "$state.png"
```

Repeat after opening a menu, dialog, tab, or other stateful surface. WinApp CLI can capture a window or element and can include popup overlays through `--capture-screen`; its inspector can filter to interactive elements when a compact action map is more useful than the full tree. [inspection modes](https://github.com/microsoft/winappCli/blob/c0578fcf5a2a1e3e7e5002e4521c446fb549365f/docs/ui-automation.md#L156-L165), [screenshot behavior](https://github.com/microsoft/winappCli/blob/c0578fcf5a2a1e3e7e5002e4521c446fb549365f/docs/ui-automation.md#L225-L241)

Prefer application-provided `AutomationId` values and control types for durable selectors. Treat names as potentially localizable, generated slugs and runtime IDs as snapshot-local, and coordinates as a last resort. Do not expect one initial tree dump to describe later dialogs or expanded menus.

## Failure boundary

All UIA-based tools share the same fundamental limit: they can only automate what the application exposes. Standard controls usually provide UIA automatically, while custom controls need their own UIA providers or automation peers. If an owned application presents an opaque canvas, improving its accessibility surface is more durable than adding image recognition. [Microsoft UIA provider guidance](https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-providersoverview), [WinUI custom automation peers](https://learn.microsoft.com/en-us/windows/apps/design/accessibility/custom-automation-peers)

When the application cannot be changed, use image matching, OCR, keyboard shortcuts, or coordinate input only for the opaque regions. These fallbacks are sensitive to layout, scaling, focus, themes, and localization, so verify their visible result with another screenshot or state check. Physical input also needs an unlocked interactive desktop and compatible privilege level; UAC, elevation mismatches, and remote desktop state can block delivery. [Microsoft UIPI troubleshooting](https://learn.microsoft.com/en-us/troubleshoot/power-platform/power-automate/desktop-flows/ui-automation/uipi-issues)

## Keep the interactive desktop after RDP

GUI automation that needs an unlocked desktop cannot rely on merely closing an RDP client. Move the active RDP session to the machine's local console with `tscon` instead. The RDP window closes, but the logged-in desktop and its processes keep running. Reconnecting by RDP moves the desktop back into RDP, so repeat the handoff after every maintenance connection. The console remains unlocked after the handoff.

In one Windows automation deployment, the interactive user was initially a standard user. Two variants failed on that host:

- running `tscon` as the interactive user without elevation returned error 5, access denied;
- running it as a separate elevated administrator, including the correct session-owner password, still returned error 5.

The verified setup on that host was to make the interactive user a local administrator, sign out and reconnect so Windows issued a new token, then elevate PowerShell as that same user. Use the built-in Administrators SID so the one-time setup does not depend on the localized Windows group name. The account below is an example:

```powershell
$admins = Get-LocalGroup -SID 'S-1-5-32-544'
Add-LocalGroupMember -Group $admins -Member 'CONTOSO\automation'
```

After signing out and reconnecting as the interactive user, open PowerShell with **Run as administrator** and confirm `whoami` still reports that same account. Start the automation, then transfer the current session without hard-coding its ID:

```powershell
$sessionId = (Get-Process -Id $PID).SessionId
tscon.exe $sessionId /dest:console
```

For repeated use, a desktop shortcut is enough. Set its target to:

```text
powershell.exe -NoProfile -WindowStyle Hidden -Command "$id=(Get-Process -Id $PID).SessionId; tscon.exe $id /dest:console"
```

Enable **Properties → Advanced → Run as administrator** on the shortcut. The user must still approve UAC because Windows gives local administrators a filtered token for ordinary processes. This shortcut was validated on that host; no wrapper batch file is needed.

Microsoft documents that `tscon` needs Full Control or the Remote Desktop Services Connect permission when controlling another session. On this host, a separately elevated local administrator did not satisfy that boundary; elevation as the session owner did. [Microsoft `tscon` documentation](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tscon), [Remote Desktop Services permissions](https://learn.microsoft.com/en-us/windows/win32/termserv/terminal-services-permissions)
