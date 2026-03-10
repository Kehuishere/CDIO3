from typing import List, Dict

def generate_answer(query: str, relevant_docs: List[Dict]):

    if not relevant_docs:
        return "Xin lỗi, tôi không tìm thấy thông tin phù hợp."

    selected_docs = relevant_docs[:3]

    meta = selected_docs[0]["metadata"]

    combined_content = "\n".join([d["content"] for d in selected_docs])

    if meta.get("type") == "product":

        brand = meta.get("brand", "Sản phẩm")
        price = meta.get("price", 0)

        try:
            formatted_price = f"{int(float(price)):,}đ"
        except:
            formatted_price = "liên hệ"

        return f"{brand}: {combined_content[:300]}... Giá tham khảo: {formatted_price}"

    elif meta.get("type") == "policy":

        return f"Thông tin cửa hàng:\n{combined_content}"

    return combined_content