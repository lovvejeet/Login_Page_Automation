def run_building_legends_tests(driver):
    try:
        
        # Click the building legends
        building_legends = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[3]/div/a[3]'))
        )
        building_legends.click()
        print("Clicked on Building Legends")
        time.sleep(5)
   
        # Click the building legends subject
        building_legends_subject = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'subject-tile'))
        )
        building_legends_subject.click()
        print("Clicked on Building Legends Subject")
        time.sleep(5)

        # Click the building legends subject chapter 
        building_legends_subject_chapter = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'chapter-rows'))
        )
        building_legends_subject_chapter.click()
        print("Clicked on Building Legends Subject Chapter")
        time.sleep(5)

        # Click the academic subject chapter pdf
        building_legends_pdf_chapter = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/button[3]'))
        )
        building_legends_pdf_chapter.click()
        print("Clicked on Building Legends PDF Chapter")
        time.sleep(5)

         # Click the academic subject chapter pdf close button
        building_legends_pdf_chapter_close = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div/div[6]/div/div[1]/button/i'))
        )
        building_legends_pdf_chapter_close.click()
        print("Closed Building Legends PDF Chapter")
        time.sleep(5)

        # Click the academic subject chapter quiz
        building_legends_chapter_quiz = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div/div[1]/div[2]/button[2]'))
        )
        building_legends_chapter_quiz.click()
        print("Clicked on Building Legends Chapter Quiz")
        time.sleep(5)
        
        # Click the academic subject chapter quiz close button
        building_legends_chapter_quiz_close = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div/span'))
        )
        building_legends_chapter_quiz_close.click()
        print("Closed Building Legends Chapter Quiz")
        time.sleep(5)

        # Click the academic subject back chapter 
        building_legends_back_chapter = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div/span'))
        )
        building_legends_back_chapter.click()
        print("Clicked on Building Legends Back Chapter")
        time.sleep(5)

        # Click the academic back button
        building_legends_back = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[1]/div[1]/div/span'))
        )
        building_legends_back.click()
        print("Clicked on Building Legends Back Button")
        time.sleep(5)

        
        result = "PASSED"
        print(f"Building Legends Tests: {result}")
        write_to_csv("N/A", "N/A", "Building Legends Tests", result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        write_to_csv("N/A", "N/A", "Building Legends Tests", "FAILED")