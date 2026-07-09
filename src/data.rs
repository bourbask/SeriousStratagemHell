use serde::Deserialize;
use std::collections::HashMap;

#[derive(Deserialize, Clone)]
pub struct Stratagem {
    pub name: String,
    pub button_inputs: Vec<String>,
}

#[derive(Deserialize)]
pub struct CombosRoot {
    pub themes: HashMap<String, Vec<Stratagem>>,
}

#[derive(Deserialize)]
#[allow(non_snake_case, dead_code)]
pub struct KeyCodesData {
    pub Up: u32,
    pub Down: u32,
    pub Left: u32,
    pub Right: u32,
}

#[derive(Deserialize)]
pub struct LevelSpeedData(pub HashMap<String, f64>);

pub fn load_combos() -> CombosRoot {
    let raw = include_str!("../data/combos.json");
    serde_json::from_str(raw).expect("Failed to parse combos.json")
}

#[allow(dead_code)]
pub fn load_key_codes() -> KeyCodesData {
    let raw = include_str!("../data/key_codes.json");
    serde_json::from_str(raw).expect("Failed to parse key_codes.json")
}

pub fn load_level_speed() -> LevelSpeedData {
    let raw = include_str!("../data/level_speed.json");
    serde_json::from_str(raw).expect("Failed to parse level_speed.json")
}
