package types

import (
	"fmt"
	"math/big"
	"reflect"
	"testing"

	"github.com/leanovate/gopter"
	"github.com/leanovate/gopter/gen"
	"github.com/leanovate/gopter/prop"
)

func int64ToBigInt(i int64) *big.Int {
	return big.NewInt(i)
}

func bigInt() gopter.Gen {
	return gen.Int64().Map(int64ToBigInt)
}

func genDec() gopter.Gen {
	return gen.Struct(reflect.TypeOf(&Dec{}), map[string]gopter.Gen{
		"Int": bigInt(),
	})
}

func TestStrToDectoStr(t *testing.T) {
	parameters := gopter.DefaultTestParameters()
	parameters.MinSuccessfulTests = 100000
	properties := gopter.NewProperties(parameters)

	properties.Property("Check String -> Dec -> String idempotence", prop.ForAll(
		// Using gopter's float generator and converting that into a string.
		func(f float64) bool {
			floatStr := fmt.Sprintf("%f.%d", f, Precision)
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
	parameters.MinSuccessfulTests = 100000
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
