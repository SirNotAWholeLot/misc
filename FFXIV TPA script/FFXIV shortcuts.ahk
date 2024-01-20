; All seems fine now

MakeCenterDot()
{
IfWinNotExist, CenterDot
{
    SysGet, m1, Monitor, 1
    m1x := (A_ScreenWidth // 2) - 6
    m1y := (A_ScreenHeight // 2.4) - 11
    CustomColor = 000000f  ; Can be any RGB color (it will be made transparent below).
    Gui, 57:+Toolwindow
    Gui, 57:+0x94C80000
    Gui, 57:-Toolwindow
    Gui, 57: +E0x20 +LastFound +AlwaysOnTop -Caption +ToolWindow  ; +ToolWindow avoids a taskbar button and an alt-tab menu item.
    Gui, 57: Color, %CustomColor%
    WinSet, TransColor, %CustomColor% 220  ; Make all pixels of this color transparent and make the text itself translucent (150)
    Gui, 57: Font, S15 CWhite, Lucida Console
    Gui, 57: Add, Text, x0 y0 w20 h20 , o
    Gui, 57: Show, x%m1x% y%m1y% w20 h20 NoActivate, CenterDot ; NoActivate avoids deactivating the currently active window.
}
}

UnmakeCenterDot()
{
	Gui, 57: Destroy
}

IsColorSimilar(SampleColor, TargetColor)
{
	SampleR := format("{:d}","0x" . substr(SampleColor,3,2))
	SampleG := format("{:d}","0x" . substr(SampleColor,5,2))
	SampleB := format("{:d}","0x" . substr(SampleColor,7,2))
	TargetR := format("{:d}","0x" . substr(TargetColor,3,2))
	TargetG := format("{:d}","0x" . substr(TargetColor,5,2))
	TargetB := format("{:d}","0x" . substr(TargetColor,7,2))
	return sqrt((SampleR - TargetR)**2 + (SampleG - TargetG)**2 + (SampleB - TargetB)**2)
}
return

IsComboReady(Chain)
{
	CoordMode, Pixel, Screen
	OffsetX := 1900
	OffsetY := 30 + (Chain-1)*135
	ComboColor := 0x99FF66
	PixelGetColor, SampleVar, OffsetX, OffsetY + 90, RGB	; Starting with the highest combo
	If IsColorSimilar(SampleVar, ComboColor) < 10		; Is the custom combo border present?
	{
		return 3
	}
	else
	{
		PixelGetColor, SampleVar, OffsetX, OffsetY + 45, RGB
		If IsColorSimilar(SampleVar, ComboColor) < 10
		{
			return 2
		}
		else
		{
			PixelGetColor, SampleVar, OffsetX, OffsetY, RGB
			If IsColorSimilar(SampleVar, ComboColor) < 10
			{
				return 1
			}
			else
			{
				return 0
			}
		}
	}
}
return

#If WinActive("FINAL FANTASY XIV")	; Always active - the only thing you can do from 'neutral' is activate TPA

; Third-person action game mode (mouselook mode) normal toggle
; WARNING: you can't use clicks normally while this is active!
*CapsLock::
If !TPAMode
{
	CoordMode, Mouse, Screen
	MouseMove, (A_ScreenWidth // 2), (A_ScreenHeight // 2.4), 0
	SendInput {click Down right}
	MakeCenterDot()
	TPAMode := 1
	TPASuspended := 0
}
else
{
	SendInput {click Up right}
	UnmakeCenterDot()
	TPAMode := 0
	TPASuspended := 0
}
return

; Suspend the whole script
RShift::Suspend

#If

; ===================================================================================================

#If (WinActive("FINAL FANTASY XIV") && (TPAMode = 1) && (TPASuspended = 0))	; Extra controls in TPA mode

; 'Activate' button: rclicks just above the PC's head = mouselook at something and hit to talk/attack
; You can move the cursor while holding R, it will click on what you're mousing over when released
*r::
{
	SendInput {click Up right}
	; TPASuspended := 1
	; UnmakeCenterDot()
	Sleep 15
	CoordMode, Mouse, Screen
	MouseMove, (A_ScreenWidth // 2), (A_ScreenHeight // 2.4), 0
	SendInput {click Down right}
	Sleep 25
	SendInput {click Up right}
	Sleep 25
	SendInput {click Down right}
	KeyWait r
	; MakeCenterDot()
	; TPASuspended := 0
}
return

; 'Target this' button: lclicks just above the PC's head = mouselook at something and hit to target
; You can move the cursor while holding C, it will click on what you're mousing over when released
*c::
{
	SendInput {click Up right}
	; TPASuspended := 1
	; UnmakeCenterDot()
	Sleep 15
	CoordMode, Mouse, Screen
	MouseMove, (A_ScreenWidth // 2), (A_ScreenHeight // 2.4), 0
	SendInput {click Down left}
	Sleep 25
	SendInput {click Up left}
	Sleep 25
	SendInput {click Down right}
	KeyWait c
	; MakeCenterDot()
	; TPASuspended := 0
}
return

; Held pause (for menuing and such)
*LAlt::
{
	SendInput {click Up right}
	Sleep 15
	CoordMode, Mouse, Screen
	MouseMove, (A_ScreenWidth // 2), (A_ScreenHeight // 2), 0
	TPASuspended := 1
}
return

; Chat exception
~*Enter::
{
	SendInput {click Up right}
	CoordMode, Mouse, Screen
	MouseMove, (A_ScreenWidth // 2), (A_ScreenHeight // 2), 0
	TPASuspended := 1
}
return

; TPAMode-specific shortcuts
; Removed out-of-TPA shortcuts because they were causing complexity issues
+*LButton::7
+*RButton::8
+*XButton2::9
+*XButton1::0
*q::5
*e::6
+*q::-
+*e::=

; Combo chain shortcuts
; Slot 1 chain-calls Hotbar 3 slots 1-3, slot 2 - Hotbar 3 slots 4-6...
*LButton up::
{
	ComboPos := IsComboReady(1)
	Switch ComboPos
	{
		Case 0: SendInput 1
		Case 1: SendInput {Numpad1}
		Case 2: SendInput {Numpad2}
		Case 3: SendInput {Numpad3}
	}
}
return
*RButton up::
{
	ComboPos := IsComboReady(2)
	Switch ComboPos
	{
		Case 0: SendInput 2
		Case 1: SendInput {Numpad4}
		Case 2: SendInput {Numpad5}
		Case 3: SendInput {Numpad6}
	}
}
return
*XButton2 up::
{
	ComboPos := IsComboReady(3)
	Switch ComboPos
	{
		Case 0: SendInput 3
		Case 1: SendInput {Numpad7}
		Case 2: SendInput {Numpad8}
		Case 3: SendInput {Numpad9}
	}
}
return
*XButton1 up::
{
	ComboPos := IsComboReady(4)
	Switch ComboPos
	{
		Case 0: SendInput 4
		Case 1: SendInput {Numpad0}
		Case 2: SendInput {NumpadDot}
		Case 3: SendInput {NumpadMult}
	}
}
return

#If

; ===================================================================================================

#If (WinActive("FINAL FANTASY XIV") && (TPAMode = 1) && (TPASuspended = 1))	; What to do when suspended - pause/exception releases

; Held pause release
*LAlt up::
{
	SendInput {click Down right}
	TPASuspended := 0
}
return

; Chat pause release
~*Enter::
{
	SendInput {click Down right}
	TPASuspended := 0
}
return
~*Escape::
{
	SendInput {click Down right}
	TPASuspended := 0
}
return

#If

; ===================================================================================================

#If (WinActive("FINAL FANTASY XIV") && (TPAMode = 1))	; AltTab is handled separately

; On alt+tab: exit mode first, then tab out - seems to have to be rather complicated to work properly
; Without this, tabbing out causes weird behavior in other windows
*Tab::
{
	SendInput {click Up right}
	UnmakeCenterDot()
	TPAMode := 0
	TPASuspended := 0
}
return

#If

/* Dev notes:

Combo chains: the extra hotbar is in a weird spot because it's not intended to be looked at by the player, only by the AHK
X should be the same for all, Y shift appears to be 45px
1:  30 1900
2:  75 1900
3: 120 1900
4: 165 1900
5: 210 1900
6: 255 1900
7: 300 1900
8: 345 1900
9: 390 1900
0: 435 1900
-: 480 1900
=: 525 1900
Custom color is 0x99FF66

; Dev: get mouse position
*`::
{
	MouseGetPos, xpos, ypos 
	MsgBox, The cursor is at X%xpos% Y%ypos%.
}
return

; Dev: get pixel colors
*`::
{
	PixelGetColor, SampleVar1, 1896, 30 
	PixelGetColor, SampleVar2, 1897, 30 
	PixelGetColor, SampleVar3, 1898, 30 
	PixelGetColor, SampleVar4, 1899, 30 
	PixelGetColor, SampleVar5, 1900, 30 
	PixelGetColor, SampleVar6, 1901, 30 
	PixelGetColor, SampleVar7, 1902, 30 
	PixelGetColor, SampleVar8, 1903, 30 
	PixelGetColor, SampleVar9, 1904, 30 
	PixelGetColor, SampleVar10, 1905, 30 
	MsgBox, The colors are`n%SampleVar1% %SampleVar2% %SampleVar3% %SampleVar4% %SampleVar5%`n%SampleVar6% %SampleVar7% %SampleVar8% %SampleVar9% %SampleVar10%
}
return

; Dev: testing the 'click' function
*`::
{
	Click, (A_ScreenWidth // 2) (A_ScreenHeight // 2.4) Left
}
return

*/