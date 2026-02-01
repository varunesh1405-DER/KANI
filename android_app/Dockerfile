FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV ANDROID_HOME=/home/builder/android-sdk
ENV ANDROID_NDK_HOME=$ANDROID_HOME/ndk/25.1.8937393
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$JAVA_HOME/bin

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python3 \
    python3-pip \
    openjdk-11-jdk-headless \
    wget \
    unzip \
    zip \
    libncurses5 \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create builder user
RUN useradd -m builder

USER builder
WORKDIR /home/builder

# Add user-installed Python packages to PATH
ENV PATH=/home/builder/.local/bin:$PATH

# Install Python packages
RUN pip3 install --user \
    buildozer \
    Cython \
    kivy \
    requests \
    pyjnius

# Download Android SDK
RUN mkdir -p $ANDROID_HOME && \
    cd $ANDROID_HOME && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip && \
    unzip -q commandlinetools-linux-9477386_latest.zip && \
    mkdir -p cmdline-tools/latest && \
    mv cmdline-tools/* cmdline-tools/latest/ 2>/dev/null || true && \
    rm commandlinetools-linux-9477386_latest.zip

# Setup Android SDK
# Create license directory and pre-accept all licenses
RUN mkdir -p $ANDROID_HOME/licenses && \
    echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > $ANDROID_HOME/licenses/android-sdk-license && \
    echo "e06d67d16eeac1a3df1505056cbda16466225357" > $ANDROID_HOME/licenses/android-sdk-preview-license && \
    echo "d56f5187479451eabf01fb78af6dfcb131b33910" > $ANDROID_HOME/licenses/mips-android-sysimage-license

# Install required SDK packages (use only proven-stable versions)
RUN $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --sdk_root=$ANDROID_HOME \
    "platforms;android-31" \
    "platform-tools" \
    "build-tools;31.0.0" \
    "ndk;25.1.8937393"

# Copy app source
COPY --chown=builder:builder . /home/builder/app
WORKDIR /home/builder/app

# Build APK
RUN ~/.local/bin/buildozer android release

# Copy output
CMD ["sh", "-c", "cp -v bin/*.apk /output/ 2>/dev/null || echo 'APK build complete'"]
