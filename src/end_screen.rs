use macroquad::prelude::*;

pub struct EndScreen;

impl EndScreen {
    pub async fn show(score: i32, rank: Option<usize>) -> bool {
        loop {
            clear_background(WHITE);

            let go = "Game Over!";
            let go_size = measure_text(go, None, 48, 1.0);
            draw_text(go, screen_width() / 2.0 - go_size.width / 2.0, 120.0, 48.0, RED);

            let score_text = format!("Score: {}", score);
            let st_size = measure_text(&score_text, None, 32u16, 1.0);
            draw_text(&score_text, screen_width() / 2.0 - st_size.width / 2.0, 210.0, 32.0, BLACK);

            if let Some(r) = rank {
                let hs = format!("New High Score! Rank #{}", r);
                let hs_size = measure_text(&hs, None, 24u16, 1.0);
                draw_text(&hs, screen_width() / 2.0 - hs_size.width / 2.0, 260.0, 24.0, GREEN);
            }

            let again = "Press SPACE to play again";
            let a_size = measure_text(again, None, 24u16, 1.0);
            draw_text(again, screen_width() / 2.0 - a_size.width / 2.0, 350.0, 24.0, DARKGRAY);

            let quit = "Press Q to quit";
            let q_size = measure_text(quit, None, 24u16, 1.0);
            draw_text(quit, screen_width() / 2.0 - q_size.width / 2.0, 390.0, 24.0, DARKGRAY);

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
