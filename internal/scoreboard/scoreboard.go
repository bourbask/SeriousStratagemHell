package scoreboard

import (
	"encoding/json"
	"os"
	"sort"
)

const (
	filePath  = "scoreboard.json"
	maxScores = 5
)

func Load() []int {
	raw, err := os.ReadFile(filePath)
	if err != nil {
		return nil
	}
	var scores []int
	if json.Unmarshal(raw, &scores) != nil {
		return nil
	}
	return scores
}

func Save(scores []int) {
	raw, _ := json.Marshal(scores)
	os.WriteFile(filePath, raw, 0644)
}

func Add(score int) *int {
	scores := Load()
	scores = append(scores, score)
	sort.Sort(sort.Reverse(sort.IntSlice(scores)))
	if len(scores) > maxScores {
		scores = scores[:maxScores]
	}
	Save(scores)
	for i, s := range scores {
		if s == score {
			r := i + 1
			return &r
		}
	}
	return nil
}
