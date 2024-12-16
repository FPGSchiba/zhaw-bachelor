#![warn(clippy::all, rust_2018_idioms)]
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] // hide console window on Windows in release

mod app;

// When compiling natively:
#[cfg(not(target_arch = "wasm32"))]
fn main() -> eframe::Result {
    env_logger::init(); // Log to stderr (if you run with `RUST_LOG=debug`).

    let native_options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([400.0, 300.0])
            .with_min_inner_size([300.0, 220.0]),
        /*
        .with_icon(
            // NOTE: Adding an icon is optional
            eframe::icon_data::from_png_bytes(&include_bytes!("../assets/icon-256.png")[..])
                .expect("Failed to load icon"),
        ),
        */
        ..Default::default()
    };

    eframe::run_native(
        "CSV Viewer",
        native_options,
        Box::new(|_cc| {
            let mut app = app::TemplateApp::default();
            let csv_result = std::fs::read_to_string("./restaurants.csv");
            app.load_csv(csv_result.unwrap().as_str(), None);
            Ok(Box::new(app))
        }),
    )
}
