# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pytest

from selenium.webdriver.common.by import By


class TestPositionAndSize(object):

    def testShouldBeAbleToDetermineTheLocationOfAnElement(self, driver, pages):
        pages.load("xhtmlTest.html")
        location = driver.find_element(By.ID, "username").location_once_scrolled_into_view
        assert location["x"] > 0
        assert location["y"] > 0

    @pytest.mark.parametrize('page', (
        'coordinates_tests/simple_page.html',
        'coordinates_tests/page_with_empty_element.html',
        'coordinates_tests/page_with_transparent_element.html',
        'coordinates_tests/page_with_hidden_element.html'),
        ids=('basic', 'empty', 'transparent', 'hidden'))
    def testShouldGetCoordinatesOfAnElement(self, page, driver, pages):
        pages.load(page)
        element = driver.find_element(By.ID, "box")
        self._check_location(element.location_once_scrolled_into_view, x=10, y=10)
        self._check_location(element.location, x=10, y=10)

    def testShouldGetCoordinatesOfAnInvisibleElement(self, driver, pages):
        pages.load("coordinates_tests/page_with_invisible_element.html")
        element = driver.find_element(By.ID, "box")
        self._check_location(element.location_once_scrolled_into_view, x=0, y=0)
        self._check_location(element.location, x=0, y=0)

    def testShouldScrollPageAndGetCoordinatesOfAnElementThatIsOutOfViewPort(self, driver, pages):
        pages.load("coordinates_tests/page_with_element_out_of_view.html")
        element = driver.find_element(By.ID, "box")
        windowHeight = driver.get_window_size()["height"]
        self._check_location(element.location_once_scrolled_into_view, x=10)
        assert 0 <= element.location_once_scrolled_into_view["y"] <= (windowHeight - 100)
        self._check_location(element.location, x=10, y=5010)

    @pytest.mark.xfail_marionette
    @pytest.mark.xfail_phantomjs
    def testShouldGetCoordinatesOfAnElementInAFrame(self, driver, pages):
        pages.load("coordinates_tests/element_in_frame.html")
        driver.switch_to_frame(driver.find_element(By.NAME, "ifr"))
        element = driver.find_element(By.ID, "box")
        self._check_location(element.location_once_scrolled_into_view, x=25, y=25)
        self._check_location(element.location, x=10, y=10)

    @pytest.mark.xfail_marionette
    @pytest.mark.xfail_phantomjs
    def testShouldGetCoordinatesOfAnElementInANestedFrame(self, driver, pages):
        pages.load("coordinates_tests/element_in_nested_frame.html")
        driver.switch_to_frame(driver.find_element(By.NAME, "ifr"))
        driver.switch_to_frame(driver.find_element(By.NAME, "ifr"))
        element = driver.find_element(By.ID, "box")
        self._check_location(element.location_once_scrolled_into_view, x=40, y=40)
        self._check_location(element.location, x=10, y=10)

    def testShouldGetCoordinatesOfAnElementWithFixedPosition(self, driver, pages):
        pages.load("coordinates_tests/page_with_fixed_element.html")
        element = driver.find_element(By.ID, "fixed")
        self._check_location(element.location_once_scrolled_into_view, y=0)
        self._check_location(element.location, y=0)

        driver.find_element(By.ID, "bottom").click()
        self._check_location(element.location_once_scrolled_into_view, y=0)
        assert element.location["y"] > 0

    def testShouldCorrectlyIdentifyThatAnElementHasWidthAndHeight(self, driver, pages):
        pages.load("xhtmlTest.html")
        shrinko = driver.find_element(By.ID, "linkId")
        size = shrinko.size
        assert size["width"] > 0
        assert size["height"] > 0

    def _check_location(self, location, **kwargs):
        try:
            # python 2.x
            expected = kwargs.viewitems()
            actual = location.viewitems()
        except AttributeError:
            # python 3.x
            expected = kwargs.items()
            actual = location.items()
        assert expected <= actual
