# Step 1: Use an official Python image as a base
FROM python:3.8-slim

# Step 2: Set working directory
WORKDIR /app

# Step 3: Install OS-level dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Install Python dependencies
COPY ./scripts/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Install the libsa4py package
RUN git clone https://github.com/saltudelft/libsa4py.git && \
    cd libsa4py && \
    pip install .

# Step 6: Copy the project files into the container
COPY . /app

# Step 7: Set environment variables (optional, if needed)

# Step 8: Define entry point (this can be a script or a command)
CMD ["bash"]