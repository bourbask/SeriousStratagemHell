package data

import (
	_ "embed"
	"encoding/json"
)

//go:embed combos.json
var combosRaw []byte

//go:embed level_speed.json
var levelSpeedRaw []byte

type Stratagem struct {
	Name         string   `json:"name"`
	ButtonInputs []string `json:"button_inputs"`
}

type CombosRoot struct {
	Themes map[string][]Stratagem `json:"themes"`
}

type LevelSpeedData map[string]float64

var (
	Combos     CombosRoot
	LevelSpeed LevelSpeedData
)

func init() {
	if err := json.Unmarshal(combosRaw, &Combos); err != nil {
		panic("failed to parse combos.json: " + err.Error())
	}
	if err := json.Unmarshal(levelSpeedRaw, &LevelSpeed); err != nil {
		panic("failed to parse level_speed.json: " + err.Error())
	}
}
