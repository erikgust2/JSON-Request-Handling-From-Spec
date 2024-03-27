
use serde::{Serialize, Deserialize};
use serde_json::Result;

#[derive(Serialize, Deserialize)]
pub struct request {
    pub A: Option<i32>,
    pub B: Option<String>,
    pub C: Option<f32>,
    pub D: Option<Vec<bool>>,
}

impl request {
    // Serializes the Rust struct into a JSON string
    pub fn serialize(&self) -> Result<String, serde_json::Error> {
        serde_json::to_string(self).unwrap()
    }

    // Deserializes the JSON string into a Rust struct
    pub fn deserialize(json_str: &str) -> Result<request, serde_json::Error> {
        serde_json::from_str(json_str)
    }
}
