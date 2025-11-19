# Build stage
FROM debian:trixie AS builder

# Install basic build tools and aptly for repo creation
RUN apt-get update && apt-get install -y \
    devscripts \
    equivs \
    blends-dev \
    aptly \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /build

# Copy package source
COPY tasks/ /build/tasks/
COPY templates/ /build/templates/
COPY src/ /build/src/
COPY config.yaml /build/config.yaml
COPY debian/ /build/debian/

# Generate debian/control before installing build dependencies
RUN /usr/share/blends-dev/blend-gen-control -F -c

# Install build dependencies using mk-build-deps
RUN apt-get update && \
    mk-build-deps --install --remove \
    --tool='apt-get -o Debug::pkgProblemResolver=yes --no-install-recommends --yes' \
    debian/control && \
    rm -rf /var/lib/apt/lists/*

# Build the packages
RUN dpkg-buildpackage -us -uc -b

# Create aptly repository
WORKDIR /repo
RUN aptly repo create -distribution=trixie -component=main d9-repo && \
    aptly repo add d9-repo /d9-*.deb && \
    aptly publish repo -skip-signing -architectures=all d9-repo

# Runtime stage
FROM debian:trixie

# Copy aptly repository from builder
COPY --from=builder /root/.aptly/public /var/aptly-repo

# Add custom repository to apt sources
RUN echo "deb [trusted=yes] file:///var/aptly-repo trixie main" > /etc/apt/sources.list.d/d9.list

# Install runtime dependencies first (since blends puts them as Recommends not Depends)
# Then install d9-tmux from custom repository (will pull in d9-common)
RUN apt-get update && \
    apt-get install -y python3 python3-jinja2 python3-yaml python3-debconf ucf && \
    apt-get install -y d9-tmux && \
    rm -rf /var/lib/apt/lists/*

# Verify installation
RUN dpkg -l | grep d9 && \
    echo && \
    cat /etc/tmux.conf

CMD ["bash"]
