import psycopg2
import json

DBS = {
    "us": ("localhost", 5432),
    "eu": ("localhost", 5433),
    "apac": ("localhost", 5434)
}

def connect(node):
    host, port = DBS[node]
    return psycopg2.connect(
        host="127.0.0.1", port=port,
        database="products",
        user="user", password="password"
    )

def compare(v1, v2):
    greater = False
    smaller = False

    for k in v1:
        if v1[k] > v2[k]: greater = True
        if v1[k] < v2[k]: smaller = True

    if greater and not smaller:
        return "SUCCESSOR"
    elif smaller and not greater:
        return "ANCESTOR"
    else:
        return "CONCURRENT"

def merge(v1, v2):
    return {k: max(v1[k], v2[k]) for k in v1}

def update_product(node, product_id, new_price):
    conn = connect(node)
    cur = conn.cursor()

    cur.execute("SELECT vector_clock FROM product_catalog WHERE id=%s", (product_id,))
    vc = cur.fetchone()[0]

    vc[node] += 1

    cur.execute("""
        UPDATE product_catalog
        SET price=%s, vector_clock=%s, last_updated_by=%s
        WHERE id=%s
    """, (new_price, json.dumps(vc), node, product_id))

    conn.commit()
    conn.close()

    replicate(node, product_id)

def replicate(source, product_id):
    source_conn = connect(source)
    cur = source_conn.cursor()

    cur.execute("SELECT * FROM product_catalog WHERE id=%s", (product_id,))
    row = cur.fetchone()

    for node in DBS:
        if node != source:
            apply_update(node, row)

def apply_update(node, row):
    conn = connect(node)
    cur = conn.cursor()

    cur.execute("SELECT vector_clock FROM product_catalog WHERE id=%s", (row[0],))
    local = cur.fetchone()[0]

    incoming = row[3]

    status = compare(local, incoming)

    if status == "SUCCESSOR":
        cur.execute("UPDATE product_catalog SET price=%s, vector_clock=%s WHERE id=%s",
                    (row[2], json.dumps(incoming), row[0]))

    elif status == "CONCURRENT":
        winner = max(row[4], "us")  # simple rule

        merged = merge(local, incoming)

        cur.execute("UPDATE product_catalog SET vector_clock=%s WHERE id=%s",
                    (json.dumps(merged), row[0]))

        cur.execute("""
            INSERT INTO conflict_log(product_id, winning_version, losing_version, resolved_by_node)
            VALUES (%s, %s, %s, %s)
        """, (row[0], json.dumps(incoming), json.dumps(local), node))

    conn.commit()
    conn.close()