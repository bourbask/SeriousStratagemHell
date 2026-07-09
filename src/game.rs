use macroquad::prelude::*;

use crate::data;

fn direction_keys(direction: &str) -> &[KeyCode] {
    match direction {
        "Up" => &[KeyCode::Up, KeyCode::Z],
        "Down" => &[KeyCode::Down, KeyCode::S],
        "Left" => &[KeyCode::Left, KeyCode::Q],
        "Right" => &[KeyCode::Right, KeyCode::D],
        _ => &[],
    }
}

fn is_direction_key(key: KeyCode) -> bool {
    matches!(key, KeyCode::Up | KeyCode::Down | KeyCode::Left | KeyCode::Right
             | KeyCode::Z | KeyCode::Q | KeyCode::S | KeyCode::D)
}

fn draw_arrow(direction: &str, cx: f32, cy: f32, size: f32, color: Color) {
    let half = size / 2.0;
    match direction {
        "Up" => draw_triangle(
            Vec2::new(cx, cy - half),
            Vec2::new(cx - half, cy + half),
            Vec2::new(cx + half, cy + half),
            color,
        ),
        "Down" => draw_triangle(
            Vec2::new(cx, cy + half),
            Vec2::new(cx - half, cy - half),
            Vec2::new(cx + half, cy - half),
            color,
        ),
        "Left" => draw_triangle(
            Vec2::new(cx - half, cy),
            Vec2::new(cx + half, cy - half),
            Vec2::new(cx + half, cy + half),
            color,
        ),
        "Right" => draw_triangle(
            Vec2::new(cx + half, cy),
            Vec2::new(cx - half, cy - half),
            Vec2::new(cx - half, cy + half),
            color,
        ),
        _ => {}
    }
}

fn get_first_pressed() -> Option<KeyCode> {
    for &key in &[
        KeyCode::Up, KeyCode::Down, KeyCode::Left, KeyCode::Right,
        KeyCode::Z, KeyCode::Q, KeyCode::S, KeyCode::D,
    ] {
        if is_key_pressed(key) {
            return Some(key);
        }
    }
    None
}

pub struct Game {
    level: i32,
    score: i32,
    theme_name: String,
    stratagem_name: String,
    combo_keys: Vec<String>,
    combo_index: usize,
    level_speed: f64,
    round_end: f64,
}

impl Game {
    pub fn new() -> Self {
        Self {
            level: 1,
            score: 0,
            theme_name: String::new(),
            stratagem_name: String::new(),
            combo_keys: Vec::new(),
            combo_index: 0,
            level_speed: 10.0,
            round_end: 0.0,
        }
    }

    fn reset(&mut self) {
        self.level = 1;
        self.score = 0;
        self.combo_keys.clear();
        self.combo_index = 0;
    }

    fn start_round(&mut self) {
        let combos = data::load_combos();
        use ::rand::Rng;
        let mut rng = ::rand::thread_rng();
        let theme_keys: Vec<&String> = combos.themes.keys().collect();
        let theme_key = theme_keys[rng.gen_range(0..theme_keys.len())].clone();
        let stratagems = &combos.themes[&theme_key];
        let stratagem = &stratagems[rng.gen_range(0..stratagems.len())];

        self.theme_name = theme_key.clone();
        self.stratagem_name = stratagem.name.clone();
        self.combo_keys = stratagem.button_inputs.clone();
        self.combo_index = 0;

        let speed_data = data::load_level_speed();
        let key = self.level.min(5).to_string();
        self.level_speed = *speed_data.0.get(&key).unwrap_or(&10.0);

        self.round_end = get_time() + self.level_speed;
    }

    pub async fn run(&mut self) -> Option<i32> {
        self.reset();
        self.start_round();

        loop {
            let now = get_time();
            if now > self.round_end {
                return Some(self.score);
            }

            if let Some(key) = get_first_pressed() {
                match self.handle_key(key) {
                    GameEvent::Advance => self.advance_round(),
                    GameEvent::GameOver => return Some(self.score),
                    GameEvent::None => {}
                }
            }

            self.draw(now);
            next_frame().await;
        }
    }

    fn handle_key(&mut self, key: KeyCode) -> GameEvent {
        let Some(direction) = self.combo_keys.get(self.combo_index) else {
            return GameEvent::None;
        };

        let valid_keys = direction_keys(direction);
        if valid_keys.contains(&key) {
            self.combo_index += 1;
            if self.combo_index >= self.combo_keys.len() {
                return GameEvent::Advance;
            }
            return GameEvent::None;
        }

        if is_direction_key(key) {
            return GameEvent::GameOver;
        }

        GameEvent::None
    }

    fn advance_round(&mut self) {
        let combo_len = self.combo_keys.len() as i32;
        self.score += combo_len * 10 * self.level;
        self.level += 1;
        self.start_round();
    }

    fn draw(&self, now: f64) {
        let mx = 50.0;
        let my = 50.0;

        draw_text(&format!("Level: {}  Score: {}", self.level, self.score),
                  mx, my, 28.0, BLACK);
        draw_text(&format!("Theme: {}", self.theme_name),
                  mx, my + 35.0, 22.0, BLACK);
        draw_text(&format!("Stratagem: {}", self.stratagem_name),
                  mx, my + 65.0, 22.0, BLACK);

        // combo arrows
        let start_x = mx;
        let arrows_y = my + 110.0;
        let cell = 55.0;

        for (i, key_name) in self.combo_keys.iter().enumerate() {
            let cx = start_x + i as f32 * cell + cell / 2.0;
            let cy = arrows_y + cell / 2.0;

            let bg = if i < self.combo_index { LIME }
                     else if i == self.combo_index { SKYBLUE }
                     else { Color::new(0.95, 0.95, 0.95, 1.0) };

            draw_rectangle(cx - cell / 2.0, cy - cell / 2.0, cell, cell, bg);
            draw_rectangle_lines(cx - cell / 2.0, cy - cell / 2.0, cell, cell, 2.0, GRAY);

            let arrow_color = if i < self.combo_index { GREEN } else { BLACK };
            draw_arrow(key_name, cx, cy, 22.0, arrow_color);
        }

        // time bar
        let bar_x = mx;
        let bar_y = my + 195.0;
        let bar_w = screen_width() - 100.0;
        let bar_h = 22.0;

        let remaining = (self.round_end - now).max(0.0);
        let ratio = (remaining / self.level_speed) as f32;

        draw_rectangle(bar_x, bar_y, bar_w, bar_h, Color::new(0.85, 0.85, 0.85, 1.0));
        draw_rectangle(bar_x, bar_y, bar_w * ratio, bar_h,
                       Color::from_rgba(
                           (255.0 * (1.0 - ratio)) as u8,
                           (255.0 * ratio) as u8, 0, 255));

        let tip = "arrow keys  or  Z Q S D";
        draw_text(tip, mx, bar_y + 45.0, 18.0, GRAY);
    }
}

enum GameEvent {
    Advance,
    GameOver,
    None,
}
