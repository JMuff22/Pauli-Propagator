Installation
------------

.. code-block:: bash

    pip install pauli-propagation

This pulls in the Rust extension ``pprop_rs`` as a prebuilt wheel (Linux
x86_64/aarch64, macOS arm64, Windows x64; Python 3.12+). On other platforms
pip builds it from source, which needs a Rust toolchain
(`rustup <https://rustup.rs/>`_).

For development, build the extension from the checkout first, then install
the package in editable mode:

.. code-block:: bash

    pip install maturin
    cd native/pprop_rs
    maturin develop --release
    cd ../..
    pip install -e .

``maturin develop`` builds ``pprop_rs`` and installs it straight into the
active virtual environment; re-run it after pulling changes to
``native/pprop_rs``.

Running the tutorial notebooks requires the ``notebooks`` extra:

.. code-block:: bash

    pip install -e ".[notebooks]"
