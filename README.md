let
    ソース = Folder.Files(""),
    AddBase64Column = Table.AddColumn(ソース, "Base64", each Binary.ToText([Content], BinaryEncoding.Base64), type text),

    // 文字列を30,000文字ずつ分割する関数
    SplitBase64 = Table.AddColumn(AddBase64Column, "Chunks", each 
        let
            base64Text = [Base64],
            chunkSize = 30000,
            numChunks = Number.RoundUp(Text.Length(base64Text) / chunkSize),
            chunks = List.Transform({0..(numChunks - 1)}, each 
                [ Index = _, Chunk = Text.Middle(base64Text, _ * chunkSize, chunkSize) ]
            )
        in
            chunks
    ),

    // 分割されたチャンクリストを展開（行として表示）
    ExpandedChunks = Table.ExpandListColumn(SplitBase64, "Chunks"),
    #"展開された Chunks" = Table.ExpandRecordColumn(ExpandedChunks, "Chunks", {"Index", "Chunk"}, {"Chunks.Index", "Chunks.Chunk"})
in
    #"展開された Chunks"



メジャー = "data:image/bmp;base64," & CONCATENATEX('画像', '画像'[Chunks.Chunk],,[Chunks.Index],ASC)


https://qiita.com/torimaro/items/32c86ff4f89c3719c57e
https://community.fabric.microsoft.com/t5/Desktop/Embed-png-image-in-powerbi-using-Base64-not-concatenating/td-p/2633844

https://qiita.com/sys_zero/items/c7fb9bed63040fc2dc96

https://www.alphabold.com/complete-guide-to-embed-images-in-power-bi-reports-part-iii/

https://blog.gbrueckl.at/2018/01/storing-images-powerbi-analysis-services-data-models/


## b

let
    // ① フォルダから BMP 画像を取得
    FolderPath = "C:\path\to\your\images\",  // ← 適宜変更
    Source = Folder.Files(FolderPath),

    // ② BMP 画像のみをフィルタリング
    FilteredBMPs = Table.SelectRows(Source, each Text.EndsWith([Name], ".bmp")),

    // ③ 必要な列を選択（ファイル名・バイナリデータ）
    GetHeader = Table.SelectColumns(FilteredBMPs, {"Name", "Content"}),

    // ④ BMP ヘッダー情報の取得（リトルエンディアン処理）
    GetWidth = Table.AddColumn(GetHeader, "Width", each 
        let bytes = Binary.ToList(Binary.Range([Content], 18, 4))
        in bytes{0} + bytes{1} * 256 + bytes{2} * 65536 + bytes{3} * 16777216, type number),

    GetHeight = Table.AddColumn(GetWidth, "Height", each 
        let bytes = Binary.ToList(Binary.Range([Content], 22, 4))
        in bytes{0} + bytes{1} * 256 + bytes{2} * 65536 + bytes{3} * 16777216, type number),

    GetBitDepth = Table.AddColumn(GetHeight, "BitDepth", each 
        let bytes = Binary.ToList(Binary.Range([Content], 28, 2))
        in bytes{0} + bytes{1} * 256, type number),

    GetDataOffset = Table.AddColumn(GetBitDepth, "PixelArrayOffset", each 
        let bytes = Binary.ToList(Binary.Range([Content], 10, 4))
        in bytes{0} + bytes{1} * 256 + bytes{2} * 65536 + bytes{3} * 16777216, type number),

    // ⑤ ピクセルデータの抽出
    GetPixelData = Table.AddColumn(GetDataOffset, "PixelData", each 
        Binary.Range([Content], [PixelArrayOffset], Binary.Length([Content]) - [PixelArrayOffset]), type binary),

    // ⑥ パディングを考慮した行サイズの計算
    GetPaddedRowSize = Table.AddColumn(GetPixelData, "PaddedRowSize", each 
        Number.RoundUp(([Width] * [BitDepth] / 8) / 4) * 4, type number),

    GetRowSize = Table.AddColumn(GetPaddedRowSize, "RowSize", each 
        ([Width] * [BitDepth] / 8), type number),

    // ⑦ BMP のピクセルデータは下から上へ保存されているので、順番を反転
    RemovePaddingAndFlip = Table.AddColumn(GetRowSize, "CorrectedPixelData", each 
        let
            pixelData = [PixelData],
            rowCount = [Height],
            rowSize = [RowSize],
            paddedRowSize = [PaddedRowSize],

            // 1行ずつ正しく取得し、順番を反転
            chunkList = List.Reverse(List.Transform(List.Numbers(0, rowCount), 
                each Binary.Range(pixelData, _ * paddedRowSize, rowSize)))
        in
            Binary.Combine(chunkList)
    , type binary),

    // ⑧ Base64 エンコード
    ConvertToBase64 = Table.AddColumn(RemovePaddingAndFlip, "Base64", each 
        Binary.ToText([CorrectedPixelData], BinaryEncoding.Base64), type text),

    // ⑨ Data URI 形式に変換
    ConvertToDataURI = Table.AddColumn(ConvertToBase64, "DataURI", each 
        "data:image/bmp;base64," & [Base64], type text),

    // ⑩ 必要な列を選択
    FinalTable = Table.SelectColumns(ConvertToDataURI, {"Name", "Width", "Height", "BitDepth", "DataURI"})
in
    FinalTable

