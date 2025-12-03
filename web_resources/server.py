import asyncio
import websockets
import json

async def handler(websocket):
    print("【接続】クライアントが接続しました")
    try:
        async for message in websocket:
            # 1. JSONをパース
            data = json.loads(message)
            
            # 2. 全ての可能性のあるキーを取得（存在しなければ None になる）
            who = data.get("who")
            turn = data.get("turn")
            
            y = data.get("y")
            x = data.get("x")
            coord = data.get("coord")
            
            # 評価値 (evalの中に score と delta がある)
            eval_data = data.get("eval")
            if eval_data:
                score = eval_data.get("score")
                delta = eval_data.get("delta")
            else:
                score = None
                delta = None
            
            # 盤面データ
            grid = data.get("grid")

            # 3. 全情報を表示
            print("\n" + "="*30)
            print(f"【受信タイプ (who)】: {who}")
            print("-" * 30)
            print(f"  Turn (手数)    : {turn}")
            print(f"  Coord (場所名) : {coord}")
            print(f"  Y, X (座標)    : {y}, {x}")
            print(f"  Score (評価値) : {score}")
            print(f"  Delta (変動値) : {delta}")
            
            # 盤面はデータが大きいので、Noneか「データあり」かを表示
            # (中身も見たい場合は print(grid) に書き換えてください)
            if grid is not None:
                print(f"  Grid (盤面)    : [データあり (8x8)]")
            else:
                print(f"  Grid (盤面)    : None")
            print("="*30)

    except websockets.exceptions.ConnectionClosed:
        print("\n【切断】クライアントが切断しました")

async def main():
    # 0.0.0.0 で待受（どこからでも接続OK）
    async with websockets.serve(handler, "127.0.0.1", 8765):
        print("サーバ待機中: ws://127.0.0.1:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())