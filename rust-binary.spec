%global rust_version 1.3.0
%global staticprefix rust-%{rust_version}-x86_64-unknown-linux-gnu

%global debug_package %{nil}
# Do not check any files in docdir for requires
%global __requires_exclude_from ^%{_bindir}/.*$

Name:           rust-binary
Version:        %{rust_version}
Release:        1%{?dist}
Summary:        The Rust Programming Language (official static build)

License:        ASL 2.0, MIT
URL:            http://www.rust-lang.org
Source0:        http://static.rust-lang.org/dist/%{staticprefix}.tar.gz

ExclusiveArch:  x86_64


%description
This is a compiler for Rust, including standard libraries, tools and
documentation.
This package is wrapping the official binary builds.


%package -n rust-binary-doc
Summary:       Documentation for rust binary
Requires:      rust-binary

%description -n rust-binary-doc
This package contains the documentation for rust binary.


%package -n    cargo-binary
Summary:       Package manager for Rust
Requires:      rust-binary

%description -n cargo-binary
This is the package manager for rust.
This package is wrapping the official binary builds.


%package -n cargo-binary-doc
Summary:     Documentation for the cargo package manager
Requires:    cargo-binary

%description -n cargo-binary-doc
This package contains the documentation for the cargo package manager.


%prep
%setup -q -n "%{staticprefix}"


%build
# Nothing

%install
./install.sh \
    --prefix=%{buildroot}%{_prefix} \
    --libdir=%{buildroot}%{_libdir} \
    --disable-ldconfig


# Create ld.so.conf file
mkdir -p %{buildroot}/%{_sysconfdir}/ld.so.conf.d
cat <<EOF | tee %{buildroot}%{_sysconfdir}/ld.so.conf.d/rust-%{_target_cpu}.conf
%{_libdir}/rustlib/
%{_libdir}/rustlib/%{_target_cpu}-unknown-linux-gnu/lib/
EOF

# Remove buildroot from manifest
sed -i "s#%{buildroot}##g" %{buildroot}%{_libdir}/rustlib/manifest-*
rm -f %{buildroot}%{_libdir}/rustlib/install.log

# Correct permission on html doc
find %{buildroot} -name *.html | xargs chmod 644
find %{buildroot} -name *.js | xargs chmod 644
find %{buildroot} -name *.woff | xargs chmod 644
find %{buildroot} -name *.css | xargs chmod 644
find %{buildroot} -name *.inc | xargs chmod 644
# Remove empty files in doc
find %{buildroot} -type f -size 0 | xargs rm -f


%post -p /sbin/ldconfig


%files
%doc COPYRIGHT README.md
%license LICENSE-APACHE LICENSE-MIT
%{_sysconfdir}/ld.so.conf.d/rust-*.conf
%{_bindir}/rustc
%{_bindir}/rustdoc
%{_bindir}/rust-gdb
%{_libdir}/rustlib/
%{_libdir}/lib*.so
%{_mandir}/man1/rust*.gz


%files -n cargo-binary
%license LICENSE-APACHE LICENSE-MIT
%{_bindir}/cargo
%{_mandir}/man1/cargo*.gz
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_cargo
%dir /usr/etc/bash_completion.d
/usr/etc/bash_completion.d/cargo


%files -n rust-binary-doc
%license LICENSE-APACHE LICENSE-MIT
%{_datadir}/doc/rust/


%files -n cargo-binary-doc
%license LICENSE-APACHE LICENSE-MIT
%{_datadir}/doc/cargo/


%changelog
* Sun Oct 18 2015 Julien Enselme <jujens@jujens.eu> - 1.3.0-1
- Uptade to 1.3.0

* Sun Jul 12 2015 Julien Enselme <jujens@jujens.eu> - 1.1.0-1
- Update to 1.1.0

* Sun Jun 07 2015 Julien Enselme <jujens@jujens.eu> - 1.0.0-1
- Update to 1.0.0

* Sun Dec 28 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.12.0-1
- Update to 0.12.0

* Sat Jul 05 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.11.0-1
- Initial package
