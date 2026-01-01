def create_prompt_from_sheet(sheet_json: dict):
    """Converts your structured character JSON into a rich AI prompt."""
    # 1. Extract high-level data
    name = sheet_json.get('name')
    clothing = sheet_json.get('clothing')
    
    # 2. Extract nested traits and style
    traits = sheet_json.get('physical_traits', {})
    style = sheet_json.get('style', {})
    
    # 3. Assign specific variables used in the template
    hair = traits.get('hair')
    eyes = traits.get('eyes')
    physique = traits.get('physique')
    art_style = style.get('art_style')
    line_weight = style.get('line_weight')
    
    # 4. Construct the template
    prompt = (
        f"[Subject: {name}] "
        f"[Identity Anchors: {hair}, {eyes}, {physique}] "
        f"[Outfit: {clothing}] "
        f"[Style: {art_style}, {line_weight}] "
        f"[Lighting: cinematic high-contrast]"
    )
    
    return prompt