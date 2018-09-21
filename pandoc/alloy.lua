local M = {}

local function is_html (format)
  return format == 'html' or format == 'html4' or format == 'html5'
end

local function is_latex (format)
  return format == 'latex'
end

local function codeblock2pdf(code, outfile)
    local tmp = os.tmpname()
    local tmpdir = string.match(tmp, "^(.*[\\/])") or "."
    local f = io.open(tmp .. ".tex", 'w')
    latex=pandoc.pipe("pygmentize", {"-l", "alloy", "-O", "full,style=alloy,linenos=true,noclasses", "-f", "latex"}, code)
    latex=latex:gsub("\\documentclass{article}","\\documentclass[preview]{standalone}")
    latex=latex:gsub("\\usepackage%[.*%]{inputenc}","")
    latex=latex:gsub("\\section%*{}","")
    f:write(latex)
    f:close()
    os.execute("pdflatex  -interaction=batchmode -output-directory=" .. tmpdir  .. " " .. tmp .. " > /dev/null 2>&1")
    os.remove(tmp .. ".tex")
    os.remove(tmp .. ".log")
    os.remove(tmp .. ".aux")
    pdf=pandoc.pipe("cat",{tmp .. ".pdf"},"")
    os.remove(tmp .. ".pdf")
    return pdf
end
local function file_exists(name)
    local f = io.open(name, 'r')
    if f ~= nil then
        io.close(f)
        return true
    else
        return false
    end
end

local function codeblock2html(code)
    return pandoc.pipe("pygmentize", {"-l", "alloy", "-O", "style=alloy,linenos=inline,noclasses", "-f", "html"}, code)
end

function M.CodeBlock(block)
    if block.classes[1] == "alloy" then
     if is_html(FORMAT) then
        local html = codeblock2html(block.text)
        return pandoc.RawBlock('html',html)
     end
     if is_latex(FORMAT) then
        local fname = pandoc.sha1(block.text) .. ".pdf"
        local pdf = codeblock2pdf(block.text, fname)
        pandoc.mediabag.insert(fname, "application/pdf", pdf)
        return pandoc.Para({pandoc.Image({pandoc.Str("Alloy source code")}, fname)})
     end
   end
   return block
end

M[1] = {
  CodeBlock = M.CodeBlock
}

return M
