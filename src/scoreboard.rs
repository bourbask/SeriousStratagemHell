use std::fs;
use std::path::Path;

const SCOREBOARD_FILE: &str = "data/scoreboard.json";
const MAX_SCORES: usize = 5;

pub fn load() -> Vec<i32> {
    if !Path::new(SCOREBOARD_FILE).exists() {
        return Vec::new();
    }
    let raw = match fs::read_to_string(SCOREBOARD_FILE) {
        Ok(s) => s,
        Err(_) => return Vec::new(),
    };
    serde_json::from_str(&raw).unwrap_or_default()
}

pub fn save(scores: &[i32]) {
    if let Ok(json) = serde_json::to_string(scores) {
        let _ = fs::write(SCOREBOARD_FILE, &json);
    }
}

pub fn add_score(score: i32) -> Option<usize> {
    let mut scores = load();
    scores.push(score);
    scores.sort_by(|a, b| b.cmp(a));
    scores.truncate(MAX_SCORES);
    save(&scores);
    scores.iter().position(|&s| s == score).map(|i| i + 1)
}
