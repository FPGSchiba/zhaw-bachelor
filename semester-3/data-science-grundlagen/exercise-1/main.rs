use csv::StringRecord;
use serde::Deserialize;
use std::{error::Error, process};

#[derive(Debug, Deserialize)]
struct Record {
    age: i32,
    sex: i8,
    bmi: f32,
    bp: f32,
    tc: f32,
    ldl: f32,
    hdl: f32,
    tch: f32,
    ltg: f32,
    glu: f32,
    prog: f32,
}

fn median(numbers: &mut Vec<f32>) -> f32 {
    numbers.sort_by(|a, b| a.partial_cmp(b).unwrap());
    if numbers.len() % 2 == 0 {
        let mid = numbers.len() / 2;
        numbers[mid]
    } else {
        let mid = numbers.len() / 2;
        numbers[mid]
    }
}

fn example() -> Result<(), Box<dyn Error>> {
    // Build the CSV reader and iterate over each record.
    let rdr = csv::Reader::from_path("./exercise-1/Diabetes-Daten.csv".to_string());
    let mut binding = rdr?;
    let mut count = 0;
    let mut num_men = 0;
    let mut num_women = 0;
    let mut ages: Vec<i32> = vec![];
    let mut absdiff: Vec<f32> = vec![];
    let mut prog: Vec<f32> = vec![];
    let header = StringRecord::from(vec![
        "age", "sex", "bmi", "bp", "tc", "ldl", "hdl", "tch", "ltg", "glu", "prog",
    ]);
    for result in binding.records() {
        // The iterator yields Result<StringRecord, Error>, so we check the
        // error here.
        let record: csv::StringRecord = result?;
        let row: Record = record.deserialize(Some(&header))?;
        ages.push(row.age);
        prog.push(row.prog);
        let est = -360.93 - 0.08 * row.age as f32 - 23.42 * row.sex as f32
            + 5.29 * row.bmi
            + 1.22 * row.bp
            - 1.56 * row.tc
            + 1.17 * row.ldl
            + 0.9 * row.hdl
            + 8.44 * row.tch
            + 71.83 * row.ltg
            + 0.49 * row.glu;
        absdiff.push((est - row.prog).abs());
        match row.sex {
            1 => num_men += 1,
            2 => num_women += 1,
            _ => println!("Sex not found."),
        }
        println!("{:?}", row);
        count += 1;
    }
    println!("Number of Rows: {}", count);
    println!("Anzahl Männer: {}", num_men);
    println!("Anzahl Frauen: {}\n", num_women);
    match ages.iter().max() {
        Some(max) => println!("Höchstes Alter: {}", max),
        None => println!("Failed to parse max age"),
    }
    match ages.iter().min() {
        Some(min) => println!("Tiefstes Alter: {}", min),
        None => println!("Failed to parse min age"),
    }
    let absdiff_mean = absdiff.iter().sum::<f32>() / absdiff.len() as f32;
    println!("Mittelwert absdiff: {:?}\n", absdiff_mean);
    println!("Median Prog: {:?}\n", median(&mut prog));
    Ok(())
}

fn main() {
    if let Err(err) = example() {
        println!("error running example: {}", err);
        process::exit(1);
    }
}
