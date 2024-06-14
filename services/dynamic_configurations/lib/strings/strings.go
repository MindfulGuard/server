package strings

import "strings"

func IsEmptyString(s string) bool {
	return len(strings.TrimSpace(s)) == 0
}
