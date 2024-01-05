from domain.model import TableStructure, Cell, TableStructureOrdered


# TODO
# Add logic to extract header with cols
# reshape to separate class
class TableLayoutCodes:
    header = 3
    col = 1
    row = 2


def process_output_from_table_layout_detector(probs, boxes) -> TableStructure:
    headers: list[Cell] = []
    cols: list[Cell] = []
    rows: list[Cell] = []
    for p, (xmin, ymin, xmax, ymax) in zip(probs, boxes.tolist()):
        cl = p.argmax()
        pos = cl.item()
        cell = Cell(xmin, ymin, xmax, ymax)
        if pos == TableLayoutCodes.header:
            headers.append(cell)
        elif pos == TableLayoutCodes.col:
            cols.append(cell)
        elif pos == TableLayoutCodes.row:
            rows.append(cell)
    table_layout = TableStructure(rows, cols, headers)
    return table_layout


def process_to_ordered_table_structure(table: TableStructure) -> TableStructureOrdered:
    cells = find_cells_data(table.columns, table.rows)
    number_of_columns = len(table.columns)
    cell_ordered_by_rows = restore_table_format(cells, number_of_columns)
    table_structure_ordered = TableStructureOrdered(cell_ordered_by_rows)
    return table_structure_ordered


def restore_table_format(cells: list[Cell], column_len: int) \
        -> list[list[Cell]]:
    cells_sorted_by_rows = sort_by_y(cells)

    result_data = []
    for i in range(0, len(cells_sorted_by_rows), column_len):
        row = sort_by_x(cells_sorted_by_rows[i:i + column_len])
        result_data.append(row)
    return result_data


def find_cells_data(cols_data: list[Cell], rows_data: list[Cell]) \
        -> list[Cell]:
    founded_cells: list[Cell] = []
    for columns in cols_data:
        for rows in rows_data:
            xmin_inter, ymin_inter, xmax_inter, ymax_inter = \
                find_intersection(columns.x_min,
                                  columns.y_min,
                                  columns.x_max,
                                  columns.y_max,
                                  rows.x_min,
                                  rows.y_min,
                                  rows.x_max,
                                  rows.y_max)
            cell = Cell(xmin_inter, ymin_inter, xmax_inter, ymax_inter)
            founded_cells.append(cell)
    return founded_cells


def sort_by_y(cells: list[Cell]) -> list[Cell]:
    return sorted(cells, key=lambda cell: cell.y_min)


def sort_by_x(cells: list[Cell]) -> list[Cell]:
    return sorted(cells, key=lambda cell: cell.x_min)


def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    """Finds the intersection of two rectangles.
    Args:
      x1: The x-coordinate of the first rectangle's top-left corner.
      y1: The y-coordinate of the first rectangle's top-left corner.
      x2: The x-coordinate of the first rectangle's bottom-right corner.
      y2: The y-coordinate of the first rectangle's bottom-right corner.
      x3: The x-coordinate of the second rectangle's top-left corner.
      y3: The y-coordinate of the second rectangle's top-left corner.
      x4: The x-coordinate of the second rectangle's bottom-right corner.
      y4: The y-coordinate of the second rectangle's bottom-right corner.
    Returns:
      A tuple of four coordinates (x1, y1, x2, y2) of the intersecting rectangle,
      or None if the two rectangles do not overlap.
    """
    if x1 > x4 or x2 < x3 or y1 > y4 or y2 < y3:
        return None
    x_min = max(x1, x3)
    x_max = min(x2, x4)
    y_min = max(y1, y3)
    y_max = min(y2, y4)
    return x_min, y_min, x_max, y_max
