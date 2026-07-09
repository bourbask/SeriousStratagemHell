mod data;
mod end_screen;
mod game;
mod menu;
mod scoreboard;

#[macroquad::main("Serious Stratagem Hell")]
async fn main() {
    let mut game = game::Game::new();

    loop {
        if !menu::Menu::run().await {
            break;
        }

        let score = game.run().await;
        match score {
            Some(s) => {
                let rank = scoreboard::add_score(s);
                if !end_screen::EndScreen::show(s, rank).await {
                    break;
                }
            }
            None => break,
        }
    }
}
