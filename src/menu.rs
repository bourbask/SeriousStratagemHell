use macroquad::prelude::*;

use crate::scoreboard;

pub struct Menu;

impl Menu {
    pub async fn run() -> bool {
        loop {
            clear_background(WHITE);

            let title = "Stratagem Hell";
            let title_size = measure_text(title, None, 48u16, 1.0);
            draw_text(title, screen_width() / 2.0 - title_size.width / 2.0, 120.0, 48.0, BLACK);

            let start = "Press SPACE to start";
            let start_size = measure_text(start, None, 24u16, 1.0);
            draw_text(start, screen_width() / 2.0 - start_size.width / 2.0, 250.0, 24.0, DARKGRAY);

            let quit = "Press Q to quit";
            let quit_size = measure_text(quit, None, 24u16, 1.0);
            draw_text(quit, screen_width() / 2.0 - quit_size.width / 2.0, 290.0, 24.0, DARKGRAY);

            let scores = scoreboard::load();
            if !scores.is_empty() {
                let hs = "-- High Scores --";
                let hs_size = measure_text(hs, None, 24u16, 1.0);
                draw_text(hs, screen_width() / 2.0 - hs_size.width / 2.0, 370.0, 24.0, BLACK);

                for (i, s) in scores.iter().enumerate() {
                    let entry = format!("{}. {}", i + 1, s);
                    let es = measure_text(&entry, None, 20u16, 1.0);
                    draw_text(&entry, screen_width() / 2.0 - es.width / 2.0,
                              410.0 + i as f32 * 36.0, 20.0, GRAY);
                }
            }

            next_frame().await;

            if is_key_pressed(KeyCode::Space) {
                return true;
            }
            if is_key_pressed(KeyCode::Q) {
                return false;
            }
        }
    }
}
