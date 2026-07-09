package game

import (
	"fmt"
	"image/color"
	"math/rand"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
	"github.com/hajimehoshi/ebiten/v2/text"
	"golang.org/x/image/font/basicfont"

	"github.com/bourbask/SeriousStratagemHell/internal/data"
	"github.com/bourbask/SeriousStratagemHell/internal/scoreboard"
)

type State int

const (
	StateMenu State = iota
	StatePlay
	StateGameOver
)

type Game struct {
	state State

	// gameplay
	level         int
	score         int
	themeName     string
	stratagemName string
	comboKeys     []string
	comboIndex    int
	levelSpeed    float64
	roundEnd      float64

	// game over
	finalScore int
	rank       *int
}

var pixel *ebiten.Image

func init() {
	pixel = ebiten.NewImage(1, 1)
	pixel.Fill(color.White)
}

func New() *Game {
	return &Game{state: StateMenu}
}

func (g *Game) Update() error {
	switch g.state {
	case StateMenu:
		if inpututil.IsKeyJustPressed(ebiten.KeySpace) {
			g.state = StatePlay
			g.startGame()
		}
		if inpututil.IsKeyJustPressed(ebiten.KeyQ) {
			return fmt.Errorf("quit")
		}

	case StatePlay:
		// time check using tick counter
		if float64(ebiten.TPS()) > g.roundEnd {
			g.gameOver()
			break
		}

		if key := pressedDirectionKey(); key != nil {
			g.handleKey(*key)
		}

	case StateGameOver:
		if inpututil.IsKeyJustPressed(ebiten.KeySpace) {
			g.state = StatePlay
			g.startGame()
		}
		if inpututil.IsKeyJustPressed(ebiten.KeyQ) {
			return fmt.Errorf("quit")
		}
	}
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	switch g.state {
	case StateMenu:
		g.drawMenu(screen)
	case StatePlay:
		g.drawPlay(screen)
	case StateGameOver:
		g.drawGameOver(screen)
	}
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return 800, 600
}

// --- Menu ---

func (g *Game) drawMenu(screen *ebiten.Image) {
	screen.Fill(color.White)
	drawCenter(screen, "Stratagem Hell", 120, 48, color.Black)
	drawCenter(screen, "Press SPACE to start", 250, 24, color.RGBA{60, 60, 60, 255})
	drawCenter(screen, "Press Q to quit", 290, 24, color.RGBA{60, 60, 60, 255})

	scores := scoreboard.Load()
	if len(scores) > 0 {
		drawCenter(screen, "-- High Scores --", 370, 24, color.Black)
		for i, s := range scores {
			drawCenter(screen, fmt.Sprintf("%d. %d", i+1, s), 410+i*36, 20, color.RGBA{80, 80, 80, 255})
		}
	}
}

// --- Gameplay ---

func (g *Game) startGame() {
	g.level = 1
	g.score = 0
	g.comboKeys = nil
	g.comboIndex = 0
	g.nextRound()
}

func (g *Game) nextRound() {
	themeKeys := make([]string, 0, len(data.Combos.Themes))
	for k := range data.Combos.Themes {
		themeKeys = append(themeKeys, k)
	}
	tk := themeKeys[rand.Intn(len(themeKeys))]
	stratagems := data.Combos.Themes[tk]
	s := stratagems[rand.Intn(len(stratagems))]

	g.themeName = tk
	g.stratagemName = s.Name
	g.comboKeys = s.ButtonInputs
	g.comboIndex = 0

	key := fmt.Sprintf("%d", min(g.level, 5))
	g.levelSpeed = data.LevelSpeed[key]
	g.roundEnd = float64(ebiten.TPS()) + g.levelSpeed
}

func (g *Game) handleKey(key ebiten.Key) {
	if g.comboIndex >= len(g.comboKeys) {
		return
	}
	expected := g.comboKeys[g.comboIndex]
	if isExpectedKey(expected, key) {
		g.comboIndex++
		if g.comboIndex >= len(g.comboKeys) {
			g.score += len(g.comboKeys) * 10 * g.level
			g.level++
			g.nextRound()
		}
		return
	}
	if isDirectionKey(key) {
		g.gameOver()
	}
}

func (g *Game) drawPlay(screen *ebiten.Image) {
	screen.Fill(color.White)
	mx, my := 50.0, 50.0

	drawText(screen, fmt.Sprintf("Level: %d  Score: %d", g.level, g.score), mx, my, 24, color.Black)
	drawText(screen, fmt.Sprintf("Theme: %s", g.themeName), mx, my+35, 20, color.Black)
	drawText(screen, fmt.Sprintf("Stratagem: %s", g.stratagemName), mx, my+65, 20, color.Black)

	// combo arrows
	arrowY := my + 110
	cell := 55.0
	for i, dir := range g.comboKeys {
		cx := mx + float64(i)*cell + cell/2
		cy := arrowY + cell/2

		var bg color.RGBA
		switch {
		case i < g.comboIndex:
			bg = color.RGBA{0, 200, 0, 255}
		case i == g.comboIndex:
			bg = color.RGBA{150, 200, 255, 255}
		default:
			bg = color.RGBA{240, 240, 240, 255}
		}
		drawFilledRect(screen, cx-cell/2, cy-cell/2, cell, cell, bg)
		drawRectLines(screen, cx-cell/2, cy-cell/2, cell, cell, color.RGBA{180, 180, 180, 255})

		arrowColor := color.RGBA{0, 0, 0, 255}
		if i < g.comboIndex {
			arrowColor = color.RGBA{0, 150, 0, 255}
		}
		drawArrow(screen, dir, cx, cy, 22, arrowColor)
	}

	// time bar
	barY := my + 195
	barW := 700.0
	barH := 22.0
	remaining := g.roundEnd - float64(ebiten.TPS())
	if remaining < 0 {
		remaining = 0
	}
	ratio := remaining / g.levelSpeed
	if ratio < 0 {
		ratio = 0
	}

	drawFilledRect(screen, 50, barY, barW, barH, color.RGBA{200, 200, 200, 255})
	r := uint8(255 * (1 - ratio))
	gr := uint8(255 * ratio)
	drawFilledRect(screen, 50, barY, barW*ratio, barH, color.RGBA{r, gr, 0, 255})

	drawText(screen, "arrow keys  or  Z Q S D", 50, barY+45, 18, color.RGBA{120, 120, 120, 255})
}

// --- Game Over ---

func (g *Game) gameOver() {
	g.finalScore = g.score
	g.rank = scoreboard.Add(g.score)
	g.state = StateGameOver
}

func (g *Game) drawGameOver(screen *ebiten.Image) {
	screen.Fill(color.White)
	drawCenter(screen, "Game Over!", 120, 48, color.RGBA{180, 0, 0, 255})
	drawCenter(screen, fmt.Sprintf("Score: %d", g.finalScore), 210, 32, color.Black)

	if g.rank != nil {
		drawCenter(screen, fmt.Sprintf("New High Score! Rank #%d", *g.rank), 260, 24, color.RGBA{0, 140, 0, 255})
	}

	drawCenter(screen, "Press SPACE to play again", 350, 24, color.RGBA{60, 60, 60, 255})
	drawCenter(screen, "Press Q to quit", 390, 24, color.RGBA{60, 60, 60, 255})
}

// --- Drawing helpers ---

func drawText(screen *ebiten.Image, str string, x, y float64, size int, clr color.Color) {
	face := basicfont.Face7x13
	text.Draw(screen, str, face, int(x), int(y)+size, clr)
}

func drawCenter(screen *ebiten.Image, str string, y, size int, clr color.Color) {
	face := basicfont.Face7x13
	bounds := text.BoundString(face, str)
	x := (800 - bounds.Dx()) / 2
	text.Draw(screen, str, face, x, y, clr)
}

func drawFilledRect(screen *ebiten.Image, x, y, w, h float64, clr color.Color) {
	ebitenutil.DrawRect(screen, x, y, w, h, clr)
}

func drawRectLines(screen *ebiten.Image, x, y, w, h float64, clr color.Color) {
	ebitenutil.DrawLine(screen, x, y, x+w, y, clr)
	ebitenutil.DrawLine(screen, x+w, y, x+w, y+h, clr)
	ebitenutil.DrawLine(screen, x+w, y+h, x, y+h, clr)
	ebitenutil.DrawLine(screen, x, y+h, x, y, clr)
}

func drawArrow(screen *ebiten.Image, dir string, cx, cy, size float64, clr color.Color) {
	var x1, y1, x2, y2, x3, y3 float64
	half := size / 2
	switch dir {
	case "Up":
		x1, y1 = cx, cy-half
		x2, y2 = cx-half, cy+half
		x3, y3 = cx+half, cy+half
	case "Down":
		x1, y1 = cx, cy+half
		x2, y2 = cx-half, cy-half
		x3, y3 = cx+half, cy-half
	case "Left":
		x1, y1 = cx-half, cy
		x2, y2 = cx+half, cy-half
		x3, y3 = cx+half, cy+half
	case "Right":
		x1, y1 = cx+half, cy
		x2, y2 = cx-half, cy-half
		x3, y3 = cx-half, cy+half
	default:
		return
	}
	drawFilledTriangle(screen, x1, y1, x2, y2, x3, y3, clr)
}

func drawFilledTriangle(screen *ebiten.Image, x1, y1, x2, y2, x3, y3 float64, clr color.Color) {
	r, g, b, a := clr.RGBA()
	rf := float32(r) / 65535
	gf := float32(g) / 65535
	bf := float32(b) / 65535
	af := float32(a) / 65535

	op := &ebiten.DrawTrianglesOptions{
		FillRule: ebiten.EvenOdd,
	}
	screen.DrawTriangles(
		[]ebiten.Vertex{
			{DstX: float32(x1), DstY: float32(y1), SrcX: 0, SrcY: 0, ColorR: rf, ColorG: gf, ColorB: bf, ColorA: af},
			{DstX: float32(x2), DstY: float32(y2), SrcX: 0, SrcY: 0, ColorR: rf, ColorG: gf, ColorB: bf, ColorA: af},
			{DstX: float32(x3), DstY: float32(y3), SrcX: 0, SrcY: 0, ColorR: rf, ColorG: gf, ColorB: bf, ColorA: af},
		},
		[]uint16{0, 1, 2},
		pixel,
		op,
	)
}

// --- Input helpers ---

func isDirectionKey(key ebiten.Key) bool {
	switch key {
	case ebiten.KeyUp, ebiten.KeyDown, ebiten.KeyLeft, ebiten.KeyRight,
		ebiten.KeyZ, ebiten.KeyQ, ebiten.KeyS, ebiten.KeyD:
		return true
	}
	return false
}

func isExpectedKey(dir string, key ebiten.Key) bool {
	switch dir {
	case "Up":
		return key == ebiten.KeyUp || key == ebiten.KeyZ
	case "Down":
		return key == ebiten.KeyDown || key == ebiten.KeyS
	case "Left":
		return key == ebiten.KeyLeft || key == ebiten.KeyQ
	case "Right":
		return key == ebiten.KeyRight || key == ebiten.KeyD
	}
	return false
}

func pressedDirectionKey() *ebiten.Key {
	for _, k := range []ebiten.Key{
		ebiten.KeyUp, ebiten.KeyDown, ebiten.KeyLeft, ebiten.KeyRight,
		ebiten.KeyZ, ebiten.KeyQ, ebiten.KeyS, ebiten.KeyD,
	} {
		if inpututil.IsKeyJustPressed(k) {
			return &k
		}
	}
	return nil
}
