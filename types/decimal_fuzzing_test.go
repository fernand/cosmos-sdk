package types

import (
	"fmt"
	"math"
	"strconv"
	"testing"

	"github.com/leanovate/gopter"
	"github.com/leanovate/gopter/gen"
	"github.com/leanovate/gopter/prop"
)

var printFloatStr = "%." + strconv.Itoa(Precision) + "f"
var smallestFloat = math.Pow10(-Precision)

// We'll use gopter's float64 generator to generate Decs.
func floatToDec(f float64) Dec {
	// Negative numbers which are < 1e-Precision should appear as
	// 0.000000000000000000 and not -0.000000000000000000
	if math.Signbit(f) == true && math.Abs(f) < smallestFloat {
		f = f * -1.0
	}
	floatStr := fmt.Sprintf(printFloatStr, f)
	d, err := NewDecFromStr(floatStr)
	if err != nil {
		return ZeroDec()
	}
	return d
}

func genDec() gopter.Gen {
	return gen.Float64().Map(floatToDec)
}

func genDecRange(min, max float64) gopter.Gen {
	return gen.Float64Range(min, max).Map(floatToDec)
}

func TestStrToDectoStr(t *testing.T) {
	parameters := gopter.DefaultTestParameters()
	parameters.MinSuccessfulTests = 100000
	properties := gopter.NewProperties(parameters)

	properties.Property("Check String -> Dec -> String idempotence", prop.ForAll(
		// Using gopter's float generator and converting that into a string.
		func(f float64) bool {
			// Negative numbers which are < 1e-Precision should appear as
			// 0.000000000000000000 and not -0.000000000000000000
			if math.Signbit(f) == true && math.Abs(f) < smallestFloat {
				f = f * -1.0
			}
			floatStr := fmt.Sprintf(printFloatStr, f)
			d, err := NewDecFromStr(floatStr)
			if err != nil {
				return true
			}
			decStr := d.String()
			return floatStr == decStr
		},
		gen.Float64(),
	))

	properties.TestingRun(t)
}
func TestDocToStrToDec(t *testing.T) {
	parameters := gopter.DefaultTestParameters()
	parameters.MinSuccessfulTests = 10000
	properties := gopter.NewProperties(parameters)

	properties.Property("Check Dec -> String -> Dec idempotence", prop.ForAll(
		// Using gopter's float generator and converting that into a string.
		func(d Dec) bool {
			decStr := d.String()
			d2, err := NewDecFromStr(decStr)
			if err != nil {
				return false
			}
			return d.Equal(d2)
		},
		genDec(),
	))

	properties.TestingRun(t)
}

func TestSmallMul(t *testing.T) {
	parameters := gopter.DefaultTestParameters()
	parameters.MinSuccessfulTests = 10000
	properties := gopter.NewProperties(parameters)

	oneDec := NewDec(1)

	properties.Property("Ensure exponentiation of decimals < 1 stays < 1", prop.ForAll(
		func(d Dec) bool {
			exp := NewDec(1)
			for i := 0; i < 1000; i++ {
				exp = exp.Mul(d)
			}
			return exp.LT(oneDec)
		},
		genDecRange(0.0, 1.0),
	))

	properties.TestingRun(t)
}
