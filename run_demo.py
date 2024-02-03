from selenium import webdriver

def simulate_button_click():
    # 指定 ChromeDriver 的路径
    
    # # 创建一个 Chrome 浏览器实例
    # driver = webdriver.Chrome(executable_path=chrome_driver_path)
    # driver = webdriver.Chrome()
    
    # 打开页面
    driver.get('http://127.0.0.1:5000')
    
    # 找到按钮元素并点击
    button = driver.find_element_by_id('demoButton')
    button.click()
    
    # 关闭浏览器
    # driver.quit()
    
    return 'Button clicked successfully'

if __name__ == '__main__':
    simulate_button_click()