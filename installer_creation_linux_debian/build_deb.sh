#!/bin/bash
set -e

echo "Building Debian package..."

PKG_NAME="git-calculator"
VERSION="1.2"
ARCH="all"
PKG_DIR="${PKG_NAME}_${VERSION}_${ARCH}"
BUILD_DIR="build_deb"

# Создаем временную структуру пакета
mkdir -p $BUILD_DIR
mkdir -p $BUILD_DIR/$PKG_DIR/DEBIAN
mkdir -p $BUILD_DIR/$PKG_DIR/opt/calculator
mkdir -p $BUILD_DIR/$PKG_DIR/usr/local/bin
mkdir -p $BUILD_DIR/$PKG_DIR/usr/share/applications

# Копируем контрольные файлы
cp DEBIAN/control $BUILD_DIR/$PKG_DIR/DEBIAN/
cp DEBIAN/postinst $BUILD_DIR/$PKG_DIR/DEBIAN/
chmod 755 $BUILD_DIR/$PKG_DIR/DEBIAN/postinst

# Копируем файлы из корня в целевую структуру пакета
# КОРРЕКТНЫЕ ПУТИ - только 1 уровень вверх!
cp ../main.py $BUILD_DIR/$PKG_DIR/opt/calculator/
cp ../functions.py $BUILD_DIR/$PKG_DIR/opt/calculator/
cp ../icon.png $BUILD_DIR/$PKG_DIR/opt/calculator/
cp ../icon.ico $BUILD_DIR/$PKG_DIR/opt/calculator/

# Создаем исполняемый скрипт
cat > $BUILD_DIR/$PKG_DIR/usr/local/bin/calculator << 'EOF'
#!/bin/bash
cd /opt/calculator
python3 main.py
EOF

chmod +x $BUILD_DIR/$PKG_DIR/usr/local/bin/calculator

# Копируем desktop файл
cp ../calculator.desktop $BUILD_DIR/$PKG_DIR/usr/share/applications/

# Устанавливаем права
chmod -R 755 $BUILD_DIR/$PKG_DIR/opt/calculator
find $BUILD_DIR/$PKG_DIR -type f -name "*.py" -exec chmod 644 {} \;

# Собираем пакет
cd $BUILD_DIR
dpkg-deb --build $PKG_DIR ../../installer/git-calculator.deb

# Очищаем
cd ..
rm -rf $BUILD_DIR

echo "Debian package created: ../installer/git-calculator.deb"