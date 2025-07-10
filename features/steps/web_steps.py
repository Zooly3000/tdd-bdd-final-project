import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ID_PREFIX = 'product_'

@when('I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)

@when('I press the "{button_name}" button')
def step_impl(context, button_name):
    element_id = button_name.lower() + '-btn'
    button = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, element_id))
    )
    button.click()

@then('I should see the message "{message}"')
def step_impl(context, message):
    body = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    assert message in body.text, f'Expected message "{message}" not found in page body.'

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)

@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)

@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    select = Select(WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    ))
    select.select_by_visible_text(text)

@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    select = Select(WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    ))
    selected_text = select.first_selected_option.text
    assert selected_text == text, f'Expected selected option "{text}" but got "{selected_text}".'

@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    assert element.get_attribute('value') == '', f'Expected empty field but found "{element.get_attribute("value")}".'

@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info(f'Copied to clipboard: {context.clipboard}')

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element_value((By.ID, element_id), text_string)
    )
    assert found, f'Expected "{text_string}" in field "{element_name}" not found.'

@then('I should see "{text}" in the results')
def step_impl(context, text):
    results = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'results'))
    )
    assert text in results.text, f'Expected "{text}" not found in results.'

@then('I should not see "{text}" in the results')
def step_impl(context, text):
    results = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, 'results'))
    )
    assert text not in results.text, f'Unexpected "{text}" found in results.'
