// 渲染 SF Symbols 为 PNG（仅 macOS）。用法：
//   swift sfrender.swift <输出目录> <weight> <#RRGGBB> <文件名:符号名> ...
import AppKit

let a = CommandLine.arguments
let outDir = a[1]
let weights: [String: NSFont.Weight] = [
    "ultraLight": .ultraLight, "thin": .thin, "light": .light,
    "regular": .regular, "medium": .medium, "semibold": .semibold, "bold": .bold]
let w = weights[a[2]] ?? .regular
let hex = a[3].hasPrefix("#") ? String(a[3].dropFirst()) : a[3]
var rgb: UInt64 = 0
Scanner(string: hex).scanHexInt64(&rgb)
let fg = NSColor(srgbRed: CGFloat((rgb >> 16) & 0xff) / 255,
                 green: CGFloat((rgb >> 8) & 0xff) / 255,
                 blue: CGFloat(rgb & 0xff) / 255, alpha: 1)
let S: CGFloat = 400, pad: CGFloat = 60

for pair in a.dropFirst(4) {
    let parts = pair.split(separator: ":", maxSplits: 1).map(String.init)
    let (name, sym) = (parts[0], parts[1])
    guard let img = NSImage(systemSymbolName: sym, accessibilityDescription: nil),
          let sized = img.withSymbolConfiguration(
              NSImage.SymbolConfiguration(pointSize: S - 2 * pad, weight: w))
    else { print("MISSING \(sym)"); continue }

    let out = NSImage(size: NSSize(width: S, height: S))
    out.lockFocus()
    let r = sized.size
    let scale = min((S - 2 * pad) / r.width, (S - 2 * pad) / r.height)
    let rect = NSRect(x: (S - r.width * scale) / 2, y: (S - r.height * scale) / 2,
                      width: r.width * scale, height: r.height * scale)
    sized.draw(in: rect)
    fg.set()
    rect.fill(using: .sourceAtop)
    out.unlockFocus()

    guard let tiff = out.tiffRepresentation, let bmp = NSBitmapImageRep(data: tiff),
          let png = bmp.representation(using: .png, properties: [:]) else { continue }
    try? png.write(to: URL(fileURLWithPath: "\(outDir)/\(name).png"))
    print("ok \(name) <- \(sym)")
}
