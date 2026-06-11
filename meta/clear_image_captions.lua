-- clear_image_captions.lua
-- Clears alt text from all images
function Image(el)
    el.caption = {}
    return el
end
