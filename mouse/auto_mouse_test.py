import pyautogui
import pyperclip

# 80%로 해야함 크기 노트북 기준
#모든 행동마다 0.5초대기
pyautogui.PAUSE = 0.2

#좌표 마우스 클릭
# for a in range(1,100):
    # pyautogui.click(236,268)

    # pyautogui.click(486,21)

    # pyautogui.sleep(30)

pyautogui.click(162,134)
pyautogui.click(196,209)

pyautogui.sleep(7)
pyperclip.copy('갱신일')
pyautogui.hotkey('ctrl', 'v')
#pyautogui.write(["r","o","d","t","l","s","d","l","f"])

pyautogui.click(386,248)
pyautogui.click(297,285)
pyautogui.click(205,301)

pyautogui.click(199,364)
pyautogui.click(1005,406)
pyautogui.click(1002,442)
pyautogui.click(1120,788)

pyautogui.click(205,340)
pyautogui.moveTo(217,444)
pyautogui.scroll(1500)

pyautogui.click(211,503)
pyautogui.click(517,532)
pyautogui.click(564,547)

pyautogui.scroll(-1500)
pyautogui.click(249,402)
pyautogui.click(342,577)
pyautogui.moveTo(333,676)
pyautogui.scroll(-1500)

pyautogui.click(323,783)
pyautogui.click(1776,958)
pyautogui.sleep(3)

pyautogui.moveTo(646,575)
pyautogui.scroll(-15000)
pyautogui.moveTo(646,575)
pyautogui.rightClick()

pyautogui.click(714,650)
pyautogui.click(1187,583)
# pyautogui.sleep(1)
# pyautogui.click(617,22)

# pyautogui.sleep(1)
# pyautogui.click(114,76)

# pyautogui.sleep(60)

#pyautogui.press("f5")