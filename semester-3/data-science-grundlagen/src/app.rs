/// We derive Deserialize/Serialize so we can persist app state on shutdown.
#[derive(serde::Deserialize, serde::Serialize)]
#[serde(default)] // if we add new fields, give them default values when deserializing old state
pub struct TemplateApp {
    reversed: bool,
    selection: std::collections::HashSet<usize>,
    checked: bool,
    header: Vec<String>,
    rows: Vec<Vec<String>>,
}

impl Default for TemplateApp {
    fn default() -> Self {
        Self {
            reversed: false,
            selection: std::collections::HashSet::new(),
            checked: false,
            header: vec![],
            rows: vec![vec![]],
        }
    }
}

impl TemplateApp {
    /// Called once before the first frame.
    pub fn new(cc: &eframe::CreationContext<'_>) -> Self {
        // This is also where you can customize the look and feel of egui using
        // `cc.egui_ctx.set_visuals` and `cc.egui_ctx.set_fonts`.

        // Load previous app state (if any).
        // Note that you must enable the `persistence` feature for this to work.
        if let Some(storage) = cc.storage {
            return eframe::get_value(storage, eframe::APP_KEY).unwrap_or_default();
        }
        Default::default()
    }

    pub fn load_csv(&mut self, csv: &str) {
        let mut record_reader = csv::Reader::from_reader(csv.as_bytes());
        let mut header_reader = csv::Reader::from_reader(csv.as_bytes());
        header_reader.headers().unwrap().iter().for_each(|s| {
            self.header.push(s.to_owned());
        });
        let mut rows = vec![];

        for result in record_reader.records() {
            let record = result.expect("Failed to read CSV record");
            rows.push(record.iter().map(|s| s.to_owned()).collect());
        }

        self.rows = rows;
    }

    fn toggle_row_selection(&mut self, row_index: usize, row_response: &egui::Response) {
        if row_response.clicked() {
            if self.selection.contains(&row_index) {
                self.selection.remove(&row_index);
            } else {
                self.selection.insert(row_index);
            }
        }
    }
}

impl eframe::App for TemplateApp {
    /// Called by the frame work to save state before shutdown.
    fn save(&mut self, storage: &mut dyn eframe::Storage) {
        eframe::set_value(storage, eframe::APP_KEY, self);
    }

    /// Called each time the UI needs repainting, which may be many times per second.
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        // Put your widgets into a `SidePanel`, `TopBottomPanel`, `CentralPanel`, `Window` or `Area`.
        // For inspiration and more examples, go to https://emilk.github.io/egui

        egui::TopBottomPanel::top("top_panel").show(ctx, |ui| {
            // The top panel is often a good place for a menu bar:

            egui::menu::bar(ui, |ui| {
                // NOTE: no File->Quit on web pages!
                let is_web = cfg!(target_arch = "wasm32");
                if !is_web {
                    ui.menu_button("File", |ui| {
                        if ui.button("Quit").clicked() {
                            ctx.send_viewport_cmd(egui::ViewportCommand::Close);
                        }
                    });
                    ui.add_space(16.0);
                }
            });
        });

        egui::CentralPanel::default().show(ctx, |ui| {
            use egui_extras::{Column, TableBuilder};

            let available_height = ui.available_height();
            let mut table = TableBuilder::new(ui)
                .striped(false)
                .resizable(false)
                .cell_layout(egui::Layout::left_to_right(egui::Align::Center))
                .min_scrolled_height(0.0)
                .max_scroll_height(available_height)
                .column(Column::auto()); // Index column allocation

            // Dynamic column allocation:
            for _ in self.header.iter() {
                table = table.column(Column::auto());
            }

            table
                .header(20.0, |mut header| {
                    header.col(|ui| {
                        egui::Sides::new().show(
                            ui,
                            |ui| {
                                ui.strong("Row");
                            },
                            |ui| {
                                self.reversed ^=
                                    ui.button(if self.reversed { "⬆" } else { "⬇" }).clicked();
                            },
                        );
                    });

                    for (_, header_content) in self.header.iter().enumerate() {
                        header.col(|ui| {
                            ui.strong(header_content);
                        });
                    }
                })
                .body(|mut body| {
                    for row_index in 0..self.rows.len() {
                        let row_index = if self.reversed {
                            self.rows.len() - 1 - row_index
                        } else {
                            row_index
                        };

                        if self.rows[row_index].len() != self.header.len() {
                            // Skip rows that don't match the header:
                            println!(
                                "Skipping row {} because it has the wrong number of columns\n",
                                row_index
                            );
                            continue;
                        }

                        body.row(18.0, |mut row| {
                            row.set_selected(self.selection.contains(&row_index));

                            // Index column
                            row.col(|ui| {
                                ui.label(row_index.to_string());
                            });

                            for (_, cell_content) in self.rows[row_index].iter().enumerate() {
                                row.col(|ui| {
                                    ui.label(cell_content);
                                });
                            }

                            self.toggle_row_selection(row_index, &row.response());
                        });
                    }
                });
        });
    }
}
