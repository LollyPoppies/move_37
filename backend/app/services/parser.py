def create_prompt_from_sheet(sheet_json: dict):
    """Converts your structured character JSON into a rich AI prompt."""
    traits = sheet_json['physical_traits']
    style = sheet_json['style']
    
    prompt = (
        f"A character sheet for a movie, style is {style['art_style']}. "
        f"The character has {traits['hair']} hair and {traits['eyes']} eyes. "
        f"Wearing {sheet_json['clothing']}. "
        f"High detail, cinematic lighting, sharp line weight."
    )
    return prompt