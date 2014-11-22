#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	kitchen
Summary:	Small, useful pieces of code to make Python coding easier
Name:		python-%{module}
Version:	1.1.1
Release:	1
License:	LGPL v2+
Group:		Development/Languages
Source0:	https://fedorahosted.org/releases/k/i/kitchen/%{module}-%{version}.tar.gz
# Source0-md5:	059d7ce048ca1d0fb53e6755145137b0
URL:		https://fedorahosted.org/kitchen/
BuildRequires:	python-modules >= 2.3.1
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with tests}
BuildRequires:	python-chardet
BuildRequires:	python-coverage
BuildRequires:	python-nose
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%endif
Suggests:	python-chardet
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
kitchen includes functions to make gettext easier to use, handling
unicode text easier (conversion with bytes, outputting xml, and
calculating how many columns a string takes), and compatibility
modules for writing code that uses Python 2.7 modules but needs to run
on Python 2.3

%prep
%setup -q -n %{module}-%{version}

# can't find origin of this import
grep -r 'from test import test_support' tests -l | xargs rm

%build
%{__python} setup.py build

%if %{with tests}
nosetests-%{py_ver} --with-coverage --cover-package kitchen
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README NEWS COPYING.LESSER docs
%dir %{py_sitescriptdir}/kitchen
%{py_sitescriptdir}/kitchen/*.py[co]
%{py_sitescriptdir}/kitchen/collections
%{py_sitescriptdir}/kitchen/i18n
%{py_sitescriptdir}/kitchen/iterutils
%{py_sitescriptdir}/kitchen/pycompat24
%{py_sitescriptdir}/kitchen/pycompat25
%{py_sitescriptdir}/kitchen/pycompat27
%{py_sitescriptdir}/kitchen/text
%{py_sitescriptdir}/kitchen/versioning
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/kitchen-%{version}*.egg-info
%endif
