# Interactive Brokers 数据获取工具示例

本目录包含展示如何使用 IBDataFetcher 类的各种示例脚本。

## 文件说明

### 1. 基础示例 (`basic_examples.py`)
简单的示例，展示如何：
- 获取当前股票数据
- 获取指定结束日期的历史股票数据

### 2. 进阶示例 (`advanced_examples.py`)
更复杂的示例，展示：
- 获取多个股票的数据
- 使用不同的市场数据类型（TRADES, BID_ASK, ADJUSTED_LAST）

### 3. 资产类别示例 (`asset_examples.py`)
不同资产类别的示例：
- 外汇数据（使用 IDEALPRO 交易所和 MIDPOINT 数据类型）
- 加密货币数据（使用 PAXOS 交易所和 AGGTRADES 数据类型）

## 使用方法

每个脚本都可以独立运行。默认使用模拟交易端口（4002）。

```bash
# 运行基础示例
python basic_examples.py

# 运行进阶示例
python advanced_examples.py

# 运行资产类别示例
python asset_examples.py
```

数据将保存在以下目录：
- `data/basic/`：基础示例数据
- `data/stocks/`：多个股票数据
- `data/types/`：不同市场数据类型
- `data/forex/`：外汇数据
- `data/crypto/`：加密货币数据
