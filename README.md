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
