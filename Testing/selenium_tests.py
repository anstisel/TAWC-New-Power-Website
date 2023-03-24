import code
from operator import truediv
from queue import Empty
import unittest, os, time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException      
basedir = os.path.abspath(os.path.dirname(__file__))

class Reuse_Functions():

  def log_into_account(self, test, user):
    time.sleep(2)
    # 3.| Enters the email 
    email = test.driver.find_element(By.ID, "username")
    email.send_keys(user[1])

    # 4.| Enters the password 
    password = test.driver.find_element(By.ID, "password")
    password.send_keys(user[2])

    # 5.| Logs in 
    test.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # 6.| Waits for page to redirect and load 
    time.sleep(2)

    # 7.| Checks the name on the nav bar 
    nickname = test.driver.find_element(By.ID, "my-nav-dropdown")
    test.assertEqual(nickname.text, user[0], "Wrong User Display")

  def log_out(self, test):
    # 5.| Logs out of the account
    test.driver.find_element(By.ID, "my-nav-dropdown").click()
    test.driver.find_element(By.XPATH, "//button[@class='dropdown-item']").click()

  def check_discussion_link(self, test, post_num, post_name):
    # 1.| Return to discussion board
    discussion = test.driver.find_element(By.LINK_TEXT, test.discusson_link)
    test.driver.execute_script("arguments[0].scrollIntoView();", discussion)
    time.sleep(0.5)
    discussion.click()
    
    # 2.| Find element 
    post = test.driver.find_element(By.XPATH, "//a[@href='/view-post/" + post_num + "']" )
    test.driver.execute_script("arguments[0].scrollIntoView();", post)
    time.sleep(0.5)
    # 3.| Enter question post page
    post.click()

    # 4.| Check if the page is correct
    page = test.driver.find_element(By.XPATH, "//h1[1]")
    test.assertEqual(page.text, post_name, "Page is not correct. ID: {0}, Name: {1}".format(post_num, post_name) )

  def submit_question(self, test, title, desc):
    # 3.| Enters the tile (will be same as username)
    question_title = test.driver.find_element(By.ID, 'title' )
    question_title.send_keys(title)

    # 4.| Enters a Question
    pref_name = test.driver.find_element(By.ID, "desc")
    pref_name.send_keys(desc)

    # 5.| Submits the Question
    test.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Submit']").click()

    # 6.| Checks if the submission was a success
    alert = test.driver.find_element(By.ID, "postSuccessAlert")
    test.assertIn("Success", alert.text, "There was a failure in posting questions")

  def submit_solution(self, test, type, comment):
    # 1.| Click the dropdown for comment type
    test.driver.find_element(By.CLASS_NAME, "form-select").click()

    # 2.| Click the comment type
    test.driver.find_element(By.XPATH, "//option[@value='" + type + "']").click()

    # 3.| Changes the name of other to comment because they are named different TT-TT |Kinda janky fix but it works| 
    if type == "other":
      type = "comment"
    
    # 4.| Finds the text area
    solution = test.driver.find_element(By.XPATH, "//textarea[@placeholder='Add a... " + type + "']")

    # 5.| Adds a comment to the text area with what solution type it is |adding comment type is just for fun and could potentially manually check if it was done|
    solution.send_keys(comment)

    # 6.| Finds the submit button and clicks it
    test.driver.find_element(By.ID, "submit").click()
  
    # 7.| Checks to see if the submission was successful
    alert = test.driver.find_element(By.ID, "solutionSuccessAlert")
    test.assertIn("Your submission is currently awaiting approval from the administrator.", alert.text, "The solution was not submitted correctly")

  def find_discussion_post(self, test, title):
    # 1.| Find the correct question that was created and accepted
    found = False
    cards = test.driver.find_elements(By.CLASS_NAME, "card")
    for j in cards:
      # 1.1.| Gets the correct question post
      heading = j.find_element(By.TAG_NAME, "h2")
      if heading.text == title:
        # 1.2.| Goes to the post page
        found = True
        button_post = j.find_element(By.ID, "to_post")
        test.driver.execute_script("arguments[0].scrollIntoView();", button_post)
        time.sleep(0.5)
        button_post.click()
        break
    return found

  def approve_reject_question_post(self, test, delim, title, action):
    # 1.| Find the recently created question
    card = test.driver.find_elements(By.CLASS_NAME, "card-body")
    for i in card:
      # 1.1.| Find the correct question post
      text = i.find_elements(By.TAG_NAME, delim)
      for j in text:
        if j.text == title:
          test.driver.execute_script("arguments[0].scrollIntoView();", j)
          time.sleep(0.5)
          # 1.2.| Approve the post
          i.find_element(By.ID, action).click()
          return

class SystemTest(unittest.TestCase):
  driver = None
  
  #Start up, links to webpage
  def setUp(self):
    self.driver = webdriver.Firefox(executable_path=os.path.join(basedir,'geckodriver.exe'))

    self.functions = Reuse_Functions()

    # URL and maximise window
    self.driver.maximize_window()
    self.driver.get('http://localhost:5001/')

    #Gets a random User
    self.user = ["22906649", "22906649@gmail.com", "Hellothere1"]
    self.admin = ["admin", "admin@coolmail.com", "Th3_B0ss"]
    #global variables
    self.title_text = "22906649 Benedyct"
    self.link_names = [["Dolphin Surgery (a)", "1"], ["Rabbit Surgery (a)", "4"], ["Pig Surgery (a)", "5"]]
    
    self.discussion_board_link = "discussionboard_link"
    self.submit_question_link = "submitpost_link"
    self.homepage_link = "Homepage"
    self.discusson_link = "Discussion"
    self.admin_link = "Admin"
    self.login_link = "Login"
    self.profile_link = "Profile"

    self.solution_types = ["solution", "clarification", "other"]



  #closes webpage when finished
  def tearDown(self):
    self.driver.close()


  #Test Navbar
  #tests the links in the top navigation bar
  def test_top_navBar(self):
    # 1.| Enter Discussion board tab
    self.driver.find_element(By.LINK_TEXT, self.discusson_link).click()

    # 2.| Log into account
    self.driver.find_element(By.LINK_TEXT, self.login_link).click()
    self.functions.log_into_account(self, self.admin)

    # 3.| Enter The Profile Page
    self.driver.find_element(By.ID, "my-nav-dropdown").click()
    self.driver.find_element(By.LINK_TEXT, self.profile_link).click()

    # 4.| Logs out of the account
    self.functions.log_out(self)

    # 5.| Return to Home Page
    self.driver.find_element(By.LINK_TEXT, self.homepage_link).click()


  #Appcentance Test 1
  #tests the link on the homepage and the links to the posts on the discussion board
  #Checks navigation on the page and if a logged in user can access the discussion pages
  def test_discussion_logged_in_user(self):
    # 1.| Log into Account
    self.driver.find_element(By.LINK_TEXT, self.login_link).click()
    self.functions.log_into_account(self, self.user)

    # 2.| For the different Questions
    for i in self.link_names:
      self.functions.check_discussion_link(self, i[1], i[0])

    # 3.| Click Home Page
    self.driver.find_element(By.LINK_TEXT, self.homepage_link).click()

    # 4.| Test submission of question
    self.driver.find_element(By.ID, self.submit_question_link).click()

    # 5.| Logs out of the account
    self.functions.log_out(self)

  
  #Checks the tabs in the discussion board
  def test_archived_tab(self):
    tabs = False
    is_post_pop = False
    is_post_arch = False

    # 1.| Enters discussion board
    self.driver.find_element(By.LINK_TEXT, self.discusson_link).click()

    # 2.| Checks the buttons for a "go to post" button, means there is content on the page
    for i in self.driver.find_elements(By.CLASS_NAME, "btn-content"):
      if i.text == "Go to post!":
        is_post_pop = True
        break
    
    # 3.| Checks if there was content on the page
    self.assertEqual(is_post_pop, True, "There are no posts on popular tab.")

    # 4.| Login to admin
    self.driver.find_element(By.LINK_TEXT, self.login_link).click()
    self.functions.log_into_account(self, self.admin)

    # 5.| Create a test post
    self.driver.find_element(By.ID, self.submit_question_link).click()
    self.functions.submit_question(self,"Test Archive", "This is a question to test archiving")
    
    # 6.| approve the test post
    self.driver.find_element(By.LINK_TEXT, self.admin_link).click()
    self.functions.approve_reject_question_post(self, "a", "Test Archive", "approve")
    discussion = self.driver.find_element(By.LINK_TEXT, self.discusson_link)
    self.driver.execute_script("arguments[0].scrollIntoView();", discussion)
    time.sleep(0.5)
    discussion.click()
    
    # 7.| archive the test post
    time.sleep(0.5)
    self.driver.find_element(By.LINK_TEXT, self.admin_link).click()
    self.driver.find_element(By.XPATH, "//*[text()='History']").click()

    found = False
    for i in self.driver.find_elements(By.CLASS_NAME, "card-body"):
      # 7.2.| Find the test post
      for test_post in i.find_elements(By.TAG_NAME, "div"):
        self.driver.execute_script("arguments[0].scrollIntoView();", test_post)
        if test_post.text == "Test Archive":
          j = i.find_element(By.CLASS_NAME, "btn-group")
          self.driver.execute_script("arguments[0].scrollIntoView();", j)
          time.sleep(0.5)
          j.click()
          
          # 7.3.| click the Archive button
          for k in i.find_elements(By.TAG_NAME, "li"):
            if k.text == "Archive":
              k.click()
              found = True
              break
          break
      if found == True:
        break
    
    # 8.| Go to discussion board
    self.driver.execute_script("arguments[0].scrollIntoView();", discussion)
    time.sleep(0.5)
    discussion.click()

    # 9.| Goes to the archived Tab
    archive_tab = self.driver.find_element(By.XPATH, "//*[text()='Archived']")
    if archive_tab != None:
      archive_tab.click()
      tabs = True

    # 10.| Checks if sucessfully entered archive tab
    self.assertEqual(tabs, True, "There was no Archived Tab")

    # 11.| Checks the buttons for a "go to post" button, means there is content on the page
    for i in self.driver.find_elements(By.CLASS_NAME, "btn-content"):
      if i.text == "Go to post!":
        is_post_arch = True
        break

    # 12.| Checks if there was content on the page
    self.assertEqual(is_post_arch, True, "There are no posts on archived tab.")


  #Acceptance Test 2
  #tests the correct submitting of questions and it appearing on the discussion board (will need to change as to check if it appears on admin page but not discussion board)
  #Checks post is made by signed in user
  def test_submit_question(self):
    # 1.| Log into account
    self.driver.find_element(By.LINK_TEXT, self.login_link).click()
    self.functions.log_into_account(self, self.user)

    # 2.| Goes to submit a Question
    self.driver.find_element(By.ID, self.submit_question_link).click()

    # 3.| Submit a test Question
    title = "Creating A New Question " + self.title_text
    self.functions.submit_question(self, title, "This is a test Queston")

    # 7.| Log out of account
    self.functions.log_out(self)


  #Will redirect page t login if user is not logged in, (this checks on submit)
  def test_restrict_access_question_submission(self):
    # 1.| Enter Submit question page
    self.driver.find_element(By.ID, self.submit_question_link).click()

    # 2.| Check if the non logged in user prompt appears
    label = self.driver.find_element(By.ID, "ModalLabel")
    self.assertEqual(label.text, "Log In", "Log in pop up not working")

    # 3.| Press the log in button | Redirects to login page
    self.driver.find_element(By.ID, "login_button").click()

    # 4.| Logs into the account
    self.functions.log_into_account(self, self.user)

    # 5.| Re enters the submit question page
    self.driver.find_element(By.ID, self.submit_question_link).click()

    # 6.| Check if it is the right page
    header = self.driver.find_element(By.XPATH, "//h1[1]")
    self.assertEqual(header.text, "Submit your post here!", "Was not able to enter post")


  #Acceptance Test 3
  #Solution submission and comments
  def test_submit_solution(self):
    # 1.| Goes into login page | Enters user into input box
    self.driver.find_element(By.LINK_TEXT, self.login_link).click()
    self.functions.log_into_account(self, self.user)

    # 2.| Go to the discussion board
    self.driver.find_element(By.LINK_TEXT, self.discusson_link).click()

    # 3.| Goes to the first post
    self.driver.find_element(By.ID, "to_post").click()

    # 4.| Goes through each comment type for submission
    for i in self.solution_types:
      comment = "This is a test " + i + ", To be moderated."
      self.functions.submit_solution(self, i, comment)

    # 5.| Logs out of account
    self.functions.log_out(self)
  

  #Expects to be redirected to login page on submission of solution
  def test_restrict_access_solution(self):
    self.driver.find_element(By.LINK_TEXT, self.discusson_link).click()

    self.driver.find_element(By.ID, "to_post").click()

    # 2.| Check if the non logged in user prompt appears
    label = self.driver.find_element(By.ID, "ModalLabel")
    self.assertEqual(label.text, "Log In", "Log in pop up not working")

    # 3.| Press the log in button | Redirects to login page
    self.driver.find_element(By.ID, "login_button").click()

    # 4.| Logs into the account
    self.functions.log_into_account(self, self.user)

    self.driver.find_element(By.LINK_TEXT, self.discusson_link).click()

    self.driver.find_element(By.ID, "to_post").click()

    page = self.driver.find_elements(By.TAG_NAME, "h3")
    self.assertEqual(page[1].text, "Leave a...", "Did not enter correct page")
    

  #Acceptance Test 4
  #Admin accept question, solution, comment
  def test_admin_moderation_accept(self):
    # 1.| need to log into an admin account
    self.driver.find_element(By.LINK_TEXT, self.login_link).click()
    self.functions.log_into_account(self, self.admin)

    # 2.| Create a question
    self.driver.find_element(By.ID, self.submit_question_link).click()
    title = "Testing Question for Accepting Moderation " + self.title_text
    self.functions.submit_question(self, title, "This is a test question to be acccepted by moderation.")

    # 3.| goes to admin page | currently just a placeholder as admin page has yet to get a link 
    self.driver.find_element(By.LINK_TEXT, self.admin_link).click()

    # 4.| Find the recently created question
    self.functions.approve_reject_question_post(self, "a", title, "approve")

    # 5.| Go to the discussion board
    discussion = self.driver.find_element(By.LINK_TEXT, self.discusson_link)
    self.driver.execute_script("arguments[0].scrollIntoView();", discussion)
    time.sleep(0.5)
    discussion.click()

    # 6.| Find the correct question that was created and accepted
    self.functions.find_discussion_post(self, title)
    
    # 7.| checks the title of the question page to see if it was the recently created question
    question_title = self.driver.find_element(By.TAG_NAME, "h1")
    self.assertEqual(question_title.text, title, "Wrong Discussion Page")

    # 8.| Log out of the account
    self.functions.log_out(self)
  

#Admin reject question, solution, comment
  def test_admin_moderation_reject(self):
    # 1.| need to log into an admin account
    self.driver.find_element(By.LINK_TEXT, self.login_link).click()
    self.functions.log_into_account(self, self.admin)

    # 2.| Create a question
    self.driver.find_element(By.ID, self.submit_question_link).click()
    title = "Testing Question for testing rejecting the Question " + self.title_text
    self.functions.submit_question(self, title, "This is a test question to be rejected by moderation.")

    # 3.| goes to admin page | currently just a placeholder as admin page has yet to get a link 
    self.driver.find_element(By.LINK_TEXT, self.admin_link).click()

    # 4.| Find the recently created question
    self.functions.approve_reject_question_post(self, "a", title, "reject")

    # 5.| Go to the discussion board
    discussion = self.driver.find_element(By.LINK_TEXT, self.discusson_link)
    self.driver.execute_script("arguments[0].scrollIntoView();", discussion)
    time.sleep(0.5)
    discussion.click()

    # 6.| Find the correct question that was created and accepted
    found = self.functions.find_discussion_post(self, title)
    self.assertEqual(found, False, "Approved the post instead of rejecting it")

    # 8.| Log out of the account
    self.functions.log_out(self)


  #Acceptance Test 5
  #Viewing of solution after posting question, If not then can't see
  def test_viewing_solution_accept(self):
    participation_text = "Please make a comment contribution to see the rest of the comments."
    comment = "This is a test comment for accepting solutions"
    element_error = False

    # 1.| Log into the account
    self.driver.find_element(By.LINK_TEXT, self.login_link).click()
    self.functions.log_into_account(self, self.admin)

    # 2.| Enter Discussion Board
    self.driver.find_element(By.ID, self.discussion_board_link).click()

    # 3.| Enter the id 5 Question page
    post = self.driver.find_element(By.XPATH, "//a[@href='/view-post/5']")
    self.driver.execute_script("arguments[0].scrollIntoView();", post)
    post.click()

    try:
      participation_alert = self.driver.find_element(By.CLASS_NAME, "participation_alert")
      self.assertIn(participation_text, participation_alert.text, "There is already a solution given by user")
    except:
      element_error = True
    
    self.assertFalse(element_error, "User already has access to the solutions")

    # 4.| Enter a new solution
    self.functions.submit_solution(self, self.solution_types[0], comment)

    # 5.| Go to the admin page
    self.driver.find_element(By.LINK_TEXT, self.admin_link).click()
    
    # 6.| Enter the solutions tab for approval
    self.driver.find_element(By.XPATH, "//*[text()='Solutions']").click()

    # 7.| Approve the just made solution
    self.functions.approve_reject_question_post(self, "div", comment, "approve")

    # 8.| Go to the discussion board
    discussion = self.driver.find_element(By.LINK_TEXT, self.discusson_link)
    self.driver.execute_script("arguments[0].scrollIntoView();", discussion)
    time.sleep(0.5)
    discussion.click()

    # 9.| Enter the previous post (The id 5 question page)
    post2 = self.driver.find_element(By.XPATH, "//a[@href='/view-post/5']")
    self.driver.execute_script("arguments[0].scrollIntoView();", post2)
    post2.click()

    # 10.| Find the solution that was approved.
    approved = False
    for comments in self.driver.find_elements(By.CLASS_NAME, "comment"):
      if comments.text == comment:
        approved = True
        break
    self.assertEqual(approved, True, "Comment was not rendered")

    try:
      participation_alert_again = self.driver.find_element(By.CLASS_NAME, "participation_alert")
      self.assertNotIn(participation_text, participation_alert_again.text, "The solution was not posted")
    except:
      pass

    # 11.| Log out of the account
    self.functions.log_out(self)


  #Viewing of solution after posting question, If not then can't see
  def test_viewing_solution_reject(self):
    participation_text = "Please make a comment contribution to see the rest of the comments."
    comment = "This is a test comment for rejecting solutions"
    element_error = False

    # 1.| Log into the account
    self.driver.find_element(By.LINK_TEXT, self.login_link).click()
    self.functions.log_into_account(self, self.admin)

    # 2.| Enter Discussion Board
    self.driver.find_element(By.LINK_TEXT, self.discusson_link).click()

    # 3.| Enter the id 4 Question page
    post = self.driver.find_element(By.XPATH, "//a[@href='/view-post/4']")
    self.driver.execute_script("arguments[0].scrollIntoView();", post)
    post.click()

    try:
      participation_alert_again = self.driver.find_element(By.CLASS_NAME, "participation_alert")
      self.assertIn(participation_text, participation_alert_again.text, "There is already a solution given by user")
    except:
      element_error = True
    
    self.assertFalse(element_error, "User already has access to the solutions")


    # 4.| Enter a new solution
    self.functions.submit_solution(self, self.solution_types[0], comment)

    # 5.| Go to the admin page
    self.driver.find_element(By.LINK_TEXT, self.admin_link).click()
    
    # 6.| Enter the solutions tab for rejection
    self.driver.find_element(By.XPATH, "//*[text()='Solutions']").click()
    time.sleep(5)
    
    # 7.| reject the just made solution
    self.functions.approve_reject_question_post(self, "div", comment, "reject")

    # 8.| Go to the discussion board
    discussion = self.driver.find_element(By.LINK_TEXT, self.discusson_link)
    self.driver.execute_script("arguments[0].scrollIntoView();", discussion)
    time.sleep(0.5)
    discussion.click()

    # 9.| Enter the previous post (The id 4 question page)
    post2 = self.driver.find_element(By.XPATH, "//a[@href='/view-post/4']")
    self.driver.execute_script("arguments[0].scrollIntoView();", post2)
    post2.click()

    try:
      participation_alert_again = self.driver.find_element(By.CLASS_NAME, "participation_alert")
      self.assertIn(participation_text, participation_alert_again.text, "There is a solution given by user")
    except:
      element_error = True
    
    self.assertFalse(element_error, "User already has access to the solutions")


    # 10.| find the solution that was rejected.
    approved = False
    for comments in self.driver.find_elements(By.CLASS_NAME, "comment"):
      if comments.text == comment:
        approved = True
        break
    self.assertEqual(approved, False, "Comment was rendered")

    # 11.| Log out of the account
    self.functions.log_out(self)

  #Acceptance Test 6
  #I can upvote the questions and solutions
  def test_up_vote(self):
    comment = "This is a solution for testing upvotes"

    # 1.| Log into the account
    self.driver.find_element(By.LINK_TEXT, self.login_link).click()
    self.functions.log_into_account(self,self.admin)

    # 2.| Go to the discussion board and enter the first post
    discussion_board = self.driver.find_element(By.ID, self.discussion_board_link)
    self.driver.execute_script("arguments[0].scrollIntoView();", discussion_board)
    discussion_board.click()
    self.driver.find_element(By.ID, "to_post").click()

    # 3.| Submit a solution
    self.functions.submit_solution(self, self.solution_types[0], comment)

    self.driver.find_element(By.LINK_TEXT, self.admin_link).click()

    # 4.| Approve the just made solution
    self.driver.find_element(By.XPATH, "//*[text()='Solutions']").click()

    self.functions.approve_reject_question_post(self, "div", comment, "approve")

    # 5.| Go back to discussion board and enter the first post
    discussion = self.driver.find_element(By.LINK_TEXT, self.discusson_link)
    self.driver.execute_script("arguments[0].scrollIntoView();", discussion)
    discussion.click()
    self.driver.find_element(By.ID, "to_post").click()

    # 6.| Find all the upvote buttons
    upvote_divs = self.driver.find_elements(By.XPATH, "//div[@class='col']")
    for upvote in upvote_divs:
      # 6.1.| Get the current number of upvotes

      current_votes = upvote.find_element(By.TAG_NAME, "span").text

      # 6.2.| Click the upvote button and get the new number of upvotes
      upvote_button = upvote.find_element(By.TAG_NAME, "button")
      self.driver.execute_script("arguments[0].scrollIntoView();", upvote_button)
      upvote_button.click()
      increase_votes = upvote.find_element(By.TAG_NAME, "span").text

      # 6.3.| Check if the upvote number increased
      self.assertGreater(increase_votes, current_votes, "Did not take give the vote")

      # 6.4.| Click he upvote button again and get the new number of upvote again
      upvote_button.click()

      final_votes = upvote.find_element(By.TAG_NAME, "span").text

      # 6.5.| Check if the upvote count went back to the previous number
      self.assertEqual(final_votes, current_votes, "Did not take away the vote")







if __name__=='__main__':
  unittest.main(verbosity=2)
