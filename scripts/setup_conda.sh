#!/bin/bash
# Conda 环境设置脚本

echo "Setting up PersonaVerse Conda environment..."

# 检查 conda
if ! command -v conda &> /dev/null; then
    echo "Conda not found. Please install Miniforge first:"
    echo "  curl -fsSL https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh -o miniforge.sh"
    echo "  bash miniforge.sh -b -p \$HOME/miniforge3"
    echo "  export PATH=\$HOME/miniforge3/bin:\$PATH"
    exit 1
fi

# 创建环境
echo "Creating conda environment 'personiverse'..."
conda env create -f environment.yml

echo ""
echo "Environment created! Activate with:"
echo "  conda activate personiverse"
echo ""
echo "Run demo:"
echo "  python scripts/run_demo.py"
