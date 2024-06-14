// +build unittests

package strings

import "testing"

func TestIsEmptyString(t *testing.T) {
	var dataEmptyString string = ""
	var dataEmptyStringWithSpaces string = "   "
	var dataNotEmptyString = "H  ello"

	if ok := IsEmptyString(dataEmptyString); !ok {
		t.Errorf("Expected: %v, result: %v", true, ok)
	}

	if ok := IsEmptyString(dataEmptyStringWithSpaces); !ok {
		t.Errorf("Expected: %v, result: %v", true, ok)
	}

	if ok := IsEmptyString(dataNotEmptyString); ok {
		t.Errorf("Expected: %v, result: %v", false, ok)
	}
}
