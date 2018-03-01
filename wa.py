#!/usr/bin/python
from Tkinter import *

from selenium import webdriver
from selenium.webdriver.common import keys

import thread
import random
import time

def main():
	w = Window()
	w.run()
	

class Window:
	def __init__(self):
		self.root = Tk()
		
		self.__createGui()
		
		self.root.protocol("WM_DELETE_WINDOW", self.__close)
		
		self.startButton.bind("<Button-1>", self.findAnswers)
		self.working = False
		
				
		self.b = webdriver.Chrome()
		self.b.get("http://webassign.net/login.html")
		
		self.__login()
		
	def run(self):
		self.root.mainloop()
		
	def __createGui(self):
		self.startButton = Button(self.root, text="Start", font=("Century Gothic", 20))
		self.startButton.pack()
		
		self.numbers = Entry(self.root)
		self.numbers.pack()
		
	def findAnswers(self, event):
		self.working = not self.working
		self.startButton["text"] = "Stop" if self.working else "Start"
		
		if self.working:
			thread.start_new_thread(self.__waScript, ())
		
	def __login(self):
		id = "{add user id here}"
		domain = "unr"
		passwd = "{Add password here}"
		
		unameIn = self.b.find_element_by_name("WebAssignUsername")
		domainIn = self.b.find_element_by_name("WebAssignInstitution")
		passIn = self.b.find_element_by_name("WebAssignPassword")
		
		unameIn.send_keys(id)
		domainIn.send_keys(domain)
		passIn.send_keys(passwd)
		
		passIn.submit()
		
	def __waScript(self):
		if len(self.b.window_handles) > 1:
			nums = self.numbers.get().split(',')
			for i in range(0, len(nums)):
				nums[i] = nums[i].lstrip() #Remove leading whitespace
			print nums
			
			self.b.switch_to_window(self.b.window_handles[1])

			while self.working:
				try:
					#Find all elements with red text, match in order to nums
					vals = self.b.find_elements_by_tag_name('font')
					curNums = []
					for n in vals:
						if len(n.text) > 0:
							curNums.append(n.text)
							
					
					if self.__compareNumbers(nums, curNums):
							
						#Get all input fields
						inputs = self.b.find_elements_by_tag_name("input")
												
						for i in inputs:
							if i.get_attribute('type') == 'text':
								i.send_keys('0')	
							
						#Enable and click show answer button
						showAnswer = self.b.find_element_by_name("Key")
						self.b.execute_script("arguments[0].disabled = false;", showAnswer)
						
						showAnswer.click()

						self.working = False
					else:
						time.sleep(random.random() / 2)
						self.b.execute_script("var x = document.getElementsByName('TryAgain')[0];x.disabled = false;x.click()")
				except:
					pass	
				
			#self.startButton["text"] = "Start"
				
	def __close(self):
		self.root.destroy()
		if self.b is not None:
			self.b.close()
		raise SystemExit()
				
	def __compareNumbers(self, qNums, practiceNums):
		try:
			for i in range(0, len(qNums)):
				if not practiceNums[i].startswith(qNums[i]):
					return False
			return True
		except:
			return False

if __name__ == "__main__":
	main()