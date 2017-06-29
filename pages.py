# -*- coding: utf-8 -*-

import logging
from time import sleep

from page_object import PageObject
from page_object.elements import Button, Link
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable, visibility_of_element_located)
from selenium.webdriver.support.wait import WebDriverWait


logger = logging.getLogger(__name__)

WAIT_TIMEOUT = 60


class KaskoCalcPage(PageObject):
    URL = "http://www.renins.com/buy/auto#edit/new/data"

    add_driver = Link(link_text="Добавить водителя")
    calculate = Button(xpath="//button/span[contains(.,'Узнать стоимость')]")

    def wait_for_preloader(self):
        sleep(1)
        WebDriverWait(self.webdriver, WAIT_TIMEOUT).until_not(
            visibility_of_element_located(
                (By.CSS_SELECTOR, "div.calc-alert_preloader"))
        )
        WebDriverWait(self.webdriver, WAIT_TIMEOUT).until_not(
            visibility_of_element_located(
                (By.CSS_SELECTOR, "div.calc-alert__container"))
        )

    def _checkbox(self, value):
        if not value:
            return

        locator = (By.XPATH,
                   "//div[@class='calc-checkbox']/label[text()='%s']" % value)

        logger.info("Looking for element by %s: <%s>", *locator)
        WebDriverWait(self.webdriver, WAIT_TIMEOUT).until(
            element_to_be_clickable(locator)).click()
        self.wait_for_preloader()

    def _label(self, name, value):
        if not value:
            return

        locator = (By.XPATH, "//input[@name='%s']/..[text()='%s']" %
                   (name, value))

        logger.info("Looking for element by %s: <%s>", *locator)
        WebDriverWait(self.webdriver, WAIT_TIMEOUT).until(
            element_to_be_clickable(locator)).click()
        self.wait_for_preloader()

    def _labels(self, name):
        locator = (By.XPATH, "//input[@name='%s']/.." % name)

        logger.info("Looking for elements by %s: <%s>", *locator)
        return self.webdriver.find_elements(*locator)

    def _select(self, data_id, value):
        if not value:
            return

        locator = (By.XPATH,
                   ("//div[@data-id='%s']"
                    "//select/option[contains(.,'%s')]" % (data_id, value)))
        logger.info("Looking for element by %s: <%s>", *locator)
        WebDriverWait(self.webdriver, WAIT_TIMEOUT).until(
            element_to_be_clickable(locator)).click()
        self.wait_for_preloader()

    def _textbox(self, name, value):
        if value is None and not str(value):
            return

        locator = (By.XPATH, "//input[@name='%s']" % name)
        element = WebDriverWait(self.webdriver, WAIT_TIMEOUT).until(
            element_to_be_clickable(locator))
        element.clear()
        element.send_keys(value)

    def city(self, value):
        for i, region in enumerate(value.split('|')):
            if i == 0:
                self._label("ownCountry[0]", region.strip())
            elif i == 1:
                self._label("additionalRegions[0]", region.strip())
            elif i == 2:
                self._label("additionalSubRegions[0]", region.strip())

    def only_kasko(self):
        self._label("PolicyType[0]", "Только КАСКО")

    def brand(self, value):
        self._label("vBrand[0]", value)

    def year(self, value):
        self._label("vYear[0]", value)

    def model(self, value):
        self._label("vModel[0]", value)

    def body_type(self):
        element = self._labels("vBodyType[0]")[0]
        WebDriverWait(element, WAIT_TIMEOUT).until(
            lambda e: e.is_displayed() and e.is_enabled())
        element.click()
        self.wait_for_preloader()

    def car_run(self, value):
        self._label("vCarRun[0]", value)

    def power(self):
        elements = self._labels("vPower[0]")
        element = elements[len(elements) // 2 - 1]
        WebDriverWait(element, WAIT_TIMEOUT).until(
            lambda e: e.is_displayed() and e.is_enabled())
        element.click()
        self.wait_for_preloader()

    def autostart(self, value):
        self._label("autostart[0]", value)

    def price(self, value):
        self._textbox("vPrice[0]", value)

    def region(self, value):
        self._label("policyBuyRegion[0]", value)

    def is_credit(self, value):
        self._label("curBank[0]", value)

    def bank(self, value):
        self._select("curBankName[0]", value)

    def antitheft(self, value):
        self._select("respPUUBrand[0]", value)

    def antitheft_model(self, value):
        self._select("respPUUModel[0]", value)

    def nolimit(self):
        self._checkbox("Без ограничений")

    def driver_age(self, i, value):
        self._textbox("drvMinAge[%d]" % i, value)

    def driver_experience(self, i, value):
        self._textbox("drvMinExp[%d]" % i, value)

    def driver_marital_status(self, i, value):
        self._label("drvMaritalStatus_Page1[%d]" % i, value)

    def driver_has_children(self, i, value):
        self._label("drvHasChildren[%d]" % i, value)

    def driver_num_of_claims(self, i, value):
        self._label("NumOfClaims[%d]" % i, value)

    def franchise(self, value):
        self._select("rFranUI[2]", value)

    @property
    def total(self):
        return self.webdriver.find_element_by_xpath(
            "//div[@class='rn-price-slider--price']").text

    @property
    def options(self):
        opts = self.webdriver.find_elements_by_xpath(
            ("//input[contains(@class, 'calc-checkbox__input_checked')]"
             "/../../../../..//span[@class='calc-packages__cell-caption']"))
        return ";".join([opt.text for opt in opts])
