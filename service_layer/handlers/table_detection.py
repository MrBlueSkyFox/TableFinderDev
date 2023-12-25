from domain.model import TableBox, Cell


def process_output_from_table_detector(detection_raw: dict) -> list[TableBox]:
    table_boxes = []  # type list[TableBox]
    for box, confidence in zip(
            detection_raw["boxes"].tolist(),
            detection_raw["scores"].tolist()
    ):
        box = Cell(box[0], box[1], box[2], box[3])
        table_box = TableBox(box, confidence)
        table_boxes.append(table_box)
    return table_boxes
