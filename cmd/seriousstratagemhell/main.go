package main

import (
	"log"

	"github.com/hajimehoshi/ebiten/v2"

	"github.com/bourbask/SeriousStratagemHell/internal/game"
)

func main() {
	ebiten.SetWindowSize(800, 600)
	ebiten.SetWindowTitle("Serious Stratagem Hell")
	g := game.New()
	if err := ebiten.RunGame(g); err != nil {
		if err.Error() == "quit" {
			return
		}
		log.Fatal(err)
	}
}
