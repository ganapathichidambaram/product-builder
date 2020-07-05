#
# spec file for package product-builder
#

%global debug_package %{nil}

Summary:        CentOS Product Builder
License:        GPL-2.0-only
Group:          System/Management
Url:            http://github.com/ganapathichidambaram/product-builder
Name:           product-builder
Conflicts:      kiwi
Conflicts:      kiwi-instsource
Version:        1.2.11
Release:        0
Provides:       kiwi-schema = 6.2
Source:         product-builder-%version.tar.xz

BuildRequires: git
Requires:       libxslt
Requires:       perl >= %{perl_version}
Requires:       perl-Class-Singleton
Requires:       perl-Config-IniFiles >= 2.49
Requires:       perl-File-Slurp
Requires:       perl-JSON
Requires:       perl-Readonly
Requires:       perl-XML-LibXML
Requires:       perl-XML-LibXML-Common
Requires:       perl-XML-SAX
Requires:       perl-libwww-perl

Provides:       kiwi-packagemanager:instsource
Provides:       system-packages:kiwi-product
Requires:       obs-build
Requires:       checkmedia
Requires:       inst-source-utils
Requires:       mkisofs
Requires:       product-builder-plugin
%ifarch %ix86 x86_64
Requires:       syslinux
%endif

%description
The CentOS product builder, builds product media (CD/DVD) for
the CentOS product portfolio. Based on kiwi perl implementation.

To be used only for product medias for CentOS 8.

%prep
%setup -q

%build
test -e /.buildenv && . /.buildenv
make CFLAGS="%{optflags}"

%install
make buildroot="%{buildroot}" \
    doc_prefix="%{buildroot}/%{_defaultdocdir}" \
    man_prefix="%{buildroot}/%{_mandir}" \
    install
./.version >"%{buildroot}/%{_datadir}/kiwi/.revision"

%if 0%{?is_opensuse}
mv %{buildroot}%{_bindir}/product-builder{.pl,}
%else
# install SLE wrapper as entry point. It doesn't really harm as the
# build flavor detected is very specific, but to avoid waste...
ln -s product-builder-sle.sh %{buildroot}%{_bindir}/product-builder
%endif

%files
%dir %{_datadir}/kiwi
%license LICENSE
%{_datadir}/kiwi/.revision
%{_datadir}/kiwi/metadata
%{_datadir}/kiwi/modules
%{_datadir}/kiwi/xsl
%{_bindir}/product-builder*

%changelog
