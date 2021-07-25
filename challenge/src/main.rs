use std::fs;
use std::io::*;
use ring::digest::{Context, SHA256};

fn main() {
    let flag = fs::read_to_string("flag.txt").unwrap();

    let mut buffer = [0; 128];
    let mut cursor = Cursor::new(&mut buffer[..]);
    write!(cursor, "This is the flag: {}", flag).unwrap();

    let mut sha256 = Context::new(&SHA256);
    sha256.update(&buffer);

    while let Ok(count) = stdin().read(&mut buffer) {
        if count == 0 { break; }
        sha256.update(&buffer);
    }
    
    println!("{:02x?}", sha256.finish());
}
